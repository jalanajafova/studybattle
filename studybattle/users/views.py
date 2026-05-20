from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    # Burada kullanıcının profil bilgilerini çekip işleyeceğiz
    # Örneğin, kullanıcı adı, kazanılan ödüller, istatistikler gibi bilgileri gösterebiliriz
    user_profile = {
        "username": request.user.username,
        "email": request.user.email,
        "rewards": ["Reward 1", "Reward 2", "Reward 3"],
        "statistics": {
            "games_played": 50,
            "wins": 30,
            "losses": 20,
        }
    }

    return render(request, "users/profile.html", {
        "user_profile": user_profile
    })

# Create your views here.
