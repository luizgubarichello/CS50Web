from ssl import SO_TYPE
from django.db import models
from django.contrib.auth.models import AbstractUser

from . import validators

# Create your models here.
class User(AbstractUser):
    cpf = models.CharField(max_length=11, validators=[validators.validate_cpf], unique=True)
    REQUIRED_FIELDS = ['cpf']


class Strategy(models.Model):
    name = models.CharField(max_length=64)
    key = models.CharField(max_length=64, unique=True)
    SWING_TRADE = 'ST'
    DAY_TRADE = 'DT'
    TYPE_CHOICES = [
        (SWING_TRADE, 'Swing Trade'),
        (DAY_TRADE, 'Day Trade')
    ]
    stype = models.CharField(max_length=2, choices=TYPE_CHOICES)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Strategy {self.id}: {self.name} ({self.stype})'

    def serializeStrat(self):
        return {
            'name': self.name,
            'type': self.stype,
        }


class StrategyStat(models.Model):
    strategy = models.OneToOneField(Strategy, on_delete=models.CASCADE, related_name='stats')
    description = models.TextField(max_length=1024)
    hit_rate = models.FloatField()
    trades_tested = models.IntegerField()
    first_trade_tested = models.DateTimeField()
    stats_currency = models.CharField(max_length=3, blank=True)
    total_profit = models.FloatField()
    max_drawdown = models.FloatField()
    recommended_margin = models.FloatField()
    gain_sequence = models.IntegerField()
    loss_sequence = models.IntegerField()
    ease_of_use = models.CharField(max_length=16)
    avg_trade_length = models.DurationField()
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Stats for Strategy {self.strategy}'


class StrategyParam(models.Model):
    strategy = models.OneToOneField(Strategy, on_delete=models.CASCADE, related_name='params')
    calls_currency = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return f'Params for Strategy {self.strategy}'


class Symbol(models.Model):
    ticker = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    calls_denomination = models.CharField(max_length=16, default='pontos')
    calls_prefix = models.CharField(max_length=4, blank=True, default='')
    added = models.DateTimeField(auto_now_add=True)
    decimal_places = models.IntegerField(default=2)

    def __str__(self):
        return f'{self.ticker}: {self.name}'


class StrategyCall(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.PROTECT, related_name='calls')
    symbol = models.ForeignKey(Symbol, on_delete=models.PROTECT, related_name='events')
    COMPRA = 'Buy'
    VENDA = 'Sell'
    DIRECTION_CHOICES = [
        (COMPRA, 'Compra'),
        (VENDA, 'Venda'),
    ]
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)
    entry_price = models.FloatField()
    target_price = models.FloatField()
    stop_price = models.FloatField()
    comment = models.TextField(blank=True)
    trade_status = models.CharField(max_length=8, default='closed')
    result = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.direction} on {self.strategy}'

    def serialize(self):
        return {
            'id': self.id,
            'strategy': {
                'name': self.strategy.name,
                'stype': self.strategy.stype,
                'currency': self.strategy.params.calls_currency,
            },
            'symbol': {
                'ticker': self.symbol.ticker,
                'denomination': self.symbol.calls_denomination,
                'prefix': self.symbol.calls_prefix,
                'decimal_places': self.symbol.decimal_places,
            },
            'direction': self.get_direction_display(),
            'entry': self.entry_price,
            'target': self.target_price,
            'stop': self.stop_price,
            'comment': self.comment,
            'trade_status': self.trade_status,
            'result': self.result,
            'timestamp': self.timestamp,
        }
