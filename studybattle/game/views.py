from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Subject,
    Question,
    PlayerProfile,
    BattleResult,
    UserBadge,
    DailyMission,
    WrongAnswer,
    ShopItem,
    UserShopItem,
    AIQuizRequest,
)


@login_required
def home(request):
    query = request.GET.get("q")
    difficulty_filter = request.GET.get("difficulty")

    subjects = Subject.objects.all()

    if query:
        subjects = subjects.filter(name__icontains=query)

    if difficulty_filter:
        subjects = subjects.filter(
            question__difficulty=difficulty_filter
        ).distinct()

    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    active_users = PlayerProfile.objects.count()
    daily_battles = BattleResult.objects.count()
    total_xp = sum(player.xp for player in PlayerProfile.objects.all())

    daily_mission = DailyMission.objects.filter(is_active=True).first()
    progress = profile.xp % 100

    for subject in subjects:
        subject.question_count = Question.objects.filter(subject=subject).count()

    return render(request, "game/home.html", {
        "subjects": subjects,
        "profile": profile,
        "active_users": active_users,
        "daily_battles": daily_battles,
        "total_xp": total_xp,
        "daily_mission": daily_mission,
        "progress": progress,
    })


@login_required
def battle(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    difficulty = request.GET.get("difficulty", "easy")

    questions = Question.objects.filter(
        subject=subject,
        difficulty=difficulty
    )[:10]

    if request.method == "POST":
        score = 0
        lives = 3
        earned_xp = 0
        earned_coin = 0
        wrong_answers = []

        for question in questions:
            user_answer = request.POST.get(str(question.id))

            if user_answer == question.correct_answer:
                score += 1
                earned_xp += question.xp_reward
                earned_coin += question.coin_reward
            else:
                lives -= 1

                WrongAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_answer=user_answer,
                    correct_answer=question.correct_answer
                )

                wrong_answers.append({
                    "question": question,
                    "selected_answer": user_answer,
                    "correct_answer": question.correct_answer,
                    "explanation": question.explanation
                })

        profile, created = PlayerProfile.objects.get_or_create(user=request.user)
        old_correct_answers = profile.correct_answers

        profile.xp += earned_xp
        profile.coin += earned_coin
        profile.total_battles += 1
        profile.correct_answers += score

        mission = DailyMission.objects.filter(is_active=True).first()

        if mission and old_correct_answers < mission.target_count <= profile.correct_answers:
            profile.xp += mission.reward_xp
            profile.coin += mission.reward_coin

        profile.update_level()
        profile.save()

        BattleResult.objects.create(
            user=request.user,
            subject=subject,
            score=score,
            earned_xp=earned_xp,
            earned_coin=earned_coin
        )

        if score >= 5 and not UserBadge.objects.filter(
            user=request.user,
            title="İlk Qələbə"
        ).exists():
            UserBadge.objects.create(
                user=request.user,
                title="İlk Qələbə",
                icon="🏅"
            )

        return render(request, "game/result.html", {
            "score": score,
            "total": questions.count(),
            "earned_xp": earned_xp,
            "earned_coin": earned_coin,
            "lives": lives,
            "wrong_answers": wrong_answers,
        })

    return render(request, "game/battle.html", {
        "subject": subject,
        "questions": questions,
        "difficulty": difficulty,
    })


@login_required
def leaderboard(request):
    players = PlayerProfile.objects.order_by("-xp")[:10]

    return render(request, "game/leaderboard.html", {
        "players": players
    })


@login_required
def profile(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        avatar = request.FILES.get("avatar")

        if avatar:
            profile.avatar = avatar
            profile.save()
            return redirect("profile")

    badges = UserBadge.objects.filter(user=request.user)

    history = BattleResult.objects.filter(
        user=request.user
    ).order_by("-date")

    wrong_answers = WrongAnswer.objects.filter(
        user=request.user
    ).order_by("-created_at")

    progress = profile.xp % 100

    return render(request, "game/profile.html", {
        "profile": profile,
        "badges": badges,
        "history": history,
        "wrong_answers": wrong_answers,
        "progress": progress,
    })


@login_required
def daily_reward(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    profile.coin += 10
    profile.streak += 1
    profile.save()

    return redirect("profile")


@login_required
def shop(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    items = ShopItem.objects.filter(is_active=True)

    owned_items = UserShopItem.objects.filter(
        user=request.user
    ).values_list("item_id", flat=True)

    return render(request, "game/shop.html", {
        "profile": profile,
        "items": items,
        "owned_items": owned_items,
    })


@login_required
def buy_item(request, item_id):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)
    item = get_object_or_404(ShopItem, id=item_id)

    already_bought = UserShopItem.objects.filter(
        user=request.user,
        item=item
    ).exists()

    if not already_bought and profile.coin >= item.price:
        profile.coin -= item.price
        profile.save()

        UserShopItem.objects.create(
            user=request.user,
            item=item
        )

    return redirect("shop")


@login_required
def ai_quiz_generator(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        topic = request.POST.get("topic")
        subject_id = request.POST.get("subject")
        difficulty = request.POST.get("difficulty")

        subject = get_object_or_404(Subject, id=subject_id)

        Question.objects.create(
            subject=subject,
            difficulty=difficulty.lower(),
            question=f"{topic} mövzusuna aid əsas anlayış hansıdır?",
            option_a="Dəyişən",
            option_b="Funksiya",
            option_c="Mövzunun əsas izahı",
            option_d="Database",
            correct_answer="C",
            explanation=f"Bu sual {topic} mövzusunun əsas məntiqini yoxlamaq üçün yaradılıb.",
            xp_reward=10,
            coin_reward=5
        )

        AIQuizRequest.objects.create(
            topic=topic,
            subject=subject,
            difficulty=difficulty
        )

        return redirect("ai_quiz_generator")

    return render(request, "game/ai_quiz_generator.html", {
        "subjects": subjects
    })