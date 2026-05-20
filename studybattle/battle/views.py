from django.shortcuts import render

def multiplayer(request):
    return render(request, "battle/multiplayer.html")
