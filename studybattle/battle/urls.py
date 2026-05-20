from django.urls import path
from . import views

urlpatterns = [
    path("multiplayer/", views.multiplayer, name="multiplayer"),
]