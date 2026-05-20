from django.shortcuts import render
from .models import Reward


def rewards_home(request):
    rewards = Reward.objects.all()

    return render(request, "rewards/home.html", {
        "rewards": rewards
    })