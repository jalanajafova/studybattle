from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=20, default="📘")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ]
    )

    explanation = models.TextField(blank=True, null=True)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="easy"
    )

    xp_reward = models.IntegerField(default=10)
    coin_reward = models.IntegerField(default=5)
    time_limit = models.IntegerField(default=30)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    xp = models.IntegerField(default=0)
    coin = models.IntegerField(default=20)
    level = models.IntegerField(default=1)
    rank = models.CharField(max_length=30, default="Bronze")
    streak = models.IntegerField(default=0)

    total_battles = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    last_played = models.DateField(blank=True, null=True)

    def accuracy(self):
        total_answers = self.correct_answers + self.wrong_answers

        if total_answers == 0:
            return 0

        return round((self.correct_answers / total_answers) * 100)

    def update_level(self):
        self.level = self.xp // 100 + 1

        if self.xp >= 1500:
            self.rank = "Legend"
        elif self.xp >= 1000:
            self.rank = "Diamond"
        elif self.xp >= 700:
            self.rank = "Gold"
        elif self.xp >= 400:
            self.rank = "Silver"
        else:
            self.rank = "Bronze"

        self.save()

    def __str__(self):
        return self.user.username


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BattleResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)

    earned_xp = models.IntegerField(default=0)
    earned_coin = models.IntegerField(default=0)

    difficulty = models.CharField(max_length=20, default="easy")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}"


class WrongAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_answer = models.CharField(max_length=1)
    correct_answer = models.CharField(max_length=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.question[:30]}"


class DailyMission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_count = models.IntegerField(default=5)
    reward_xp = models.IntegerField(default=20)
    reward_coin = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class WrongAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)
    correct_answer = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class DailyMission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    target_count = models.IntegerField(default=5)
    reward_xp = models.IntegerField(default=20)
    reward_coin = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ShopItem(models.Model):
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    price = models.IntegerField(default=50)
    icon = models.CharField(max_length=20, default="🎁")

    def __str__(self):
        return self.name


class UserShopItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
class WrongAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, blank=True, null=True)
    correct_answer = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.question[:30]}"
class ShopItem(models.Model):
    ITEM_TYPES = [
        ("frame", "Avatar Frame"),
        ("badge", "Badge"),
        ("glow", "Glow Effect"),
    ]

    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    price = models.IntegerField(default=50)
    icon = models.CharField(max_length=20, default="🎁")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserShopItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"


class AIQuizRequest(models.Model):
    topic = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, default="easy")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic