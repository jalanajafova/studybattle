from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def multiplayer(request):
    return render(request, "battle/multiplayer.html")

def multiplayer(request):
    return render(request, "battle/multiplayer.html")
