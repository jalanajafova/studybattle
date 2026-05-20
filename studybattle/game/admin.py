from django.contrib import admin
from .models import (
    Subject,
    Question,
    PlayerProfile,
    BattleResult,
    UserBadge,
    WrongAnswer,
    DailyMission,
    ShopItem,
    UserShopItem,
    AIQuizRequest,
)

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(PlayerProfile)
admin.site.register(BattleResult)
admin.site.register(UserBadge)
admin.site.register(WrongAnswer)
admin.site.register(DailyMission)
admin.site.register(ShopItem)
admin.site.register(UserShopItem)
admin.site.register(AIQuizRequest)