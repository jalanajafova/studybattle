from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ai_home(request):

    response = ""

    if request.method == "POST":

        question = request.POST.get("question")

        if "python" in question.lower():
            response = "Python çox güclü proqramlaşdırma dilidir."

        elif "django" in question.lower():
            response = "Django Python frameworküdür."

        else:
            response = "AI müəllim cavabı hazırladı 🚀"

    return render(request, "ai_teacher/ai_home.html", {
        "response": response
    })