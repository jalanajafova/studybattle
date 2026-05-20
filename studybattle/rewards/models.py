from django.db import models
from django.contrib.auth.models import User


class Reward(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=20)
    description = models.TextField()
    xp_required = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username