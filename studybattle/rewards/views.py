from django.shortcuts import render
from .models import Reward
from django.contrib.auth.decorators import login_required

@login_required
def multiplayer(request):
    return render(request, "game/multiplayer.html")

def rewards_home(request):
    rewards = Reward.objects.all()

    return render(request, "rewards/home.html", {
        "rewards": rewards
    })