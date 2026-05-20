from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def leaderboard(request):
    # Burada liderlik tablosu verilerini çekip işleyeceğiz
    # Örneğin, en yüksek puanlara sahip oyuncuları sıralayabiliriz
    leaderboard_data = [
        {"username": "Player1", "score": 1500},
        {"username": "Player2", "score": 1200},
        {"username": "Player3", "score": 900},
    ]

    return render(request, "leaderboard/leaderboard.html", {
        "leaderboard_data": leaderboard_data
    })

# Create your views here.
