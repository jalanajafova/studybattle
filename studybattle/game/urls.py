from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("battle/<int:subject_id>/", views.battle, name="battle"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("profile/", views.profile, name="profile"),
    path("daily-reward/", views.daily_reward, name="daily_reward"),
    path("shop/", views.shop, name="shop"),
    path("shop/buy/<int:item_id>/", views.buy_item, name="buy_item"),
    path("ai-generator/", views.ai_quiz_generator, name="ai_quiz_generator"),
]