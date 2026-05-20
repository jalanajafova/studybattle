from django.urls import path
from .views import rewards_home

urlpatterns = [
    path('', rewards_home, name="rewards"),
]