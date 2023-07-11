from django.contrib import admin

from .models import User, Strategy, StrategyStat, StrategyParam, Symbol, StrategyCall

# Register your models here.
admin.site.register(User)
admin.site.register(Strategy)
admin.site.register(StrategyStat)
admin.site.register(StrategyParam)
admin.site.register(Symbol)
admin.site.register(StrategyCall)
