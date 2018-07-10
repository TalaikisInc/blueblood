from peewee import CharField, ForeignKeyField, SmallIntegerField, DecimalField, JSONField
from peewee_extra_fields import EnumField

from . import BaseModel


class AlphaOwner(BaseModel):
    name = CharField()
    email = CharField()

    class Meta:
        indexes = (
            (('name', 'email'), True)
        )

class Alpha(BaseModel):
    name = CharField(unique=True)
    owner = ForeignKeyField(AlphaOwner, backref='alphas')

class Strategy(BaseModel):
    alpha = ForeignKeyField(Alpha, backref='strategies')
    rule = SmallIntegerField()
    param = SmallIntegerField()

    class Meta:
        indexes = (
            (('alpha', 'rule'), True)
        )

class Stats(BaseModel):
    strategy = ForeignKeyField(Strategy, backref='stats')
    max_dd = DecimalField(decimal_places=2, auto_round=True)
    beta = DecimalField(decimal_places=2, auto_round=True)
    vol = DecimalField(decimal_places=2, auto_round=True)
    treynor = DecimalField(decimal_places=2, auto_round=True)
    sharpe_ratio = DecimalField(decimal_places=2, auto_round=True)
    ir = DecimalField(decimal_places=2, auto_round=True)
    modigliani = DecimalField(decimal_places=2, auto_round=True)
    var = DecimalField(decimal_places=2, auto_round=True)
    cvar = DecimalField(decimal_places=2, auto_round=True)
    excess_var = DecimalField(decimal_places=2, auto_round=True)
    conditional_sharpe = DecimalField(decimal_places=2, auto_round=True)
    omega_ratio = DecimalField(decimal_places=2, auto_round=True)
    sortino = DecimalField(decimal_places=2, auto_round=True)
    kappa_three = DecimalField(decimal_places=2, auto_round=True)
    gain_loss = DecimalField(decimal_places=2, auto_round=True)
    upside_potential = DecimalField(decimal_places=2, auto_round=True)
    calmar = DecimalField(decimal_places=2, auto_round=True)
    average_dd = DecimalField(decimal_places=2, auto_round=True)
    average_dd_squared = DecimalField(decimal_places=2, auto_round=True)
    sterling_ration = DecimalField(decimal_places=2, auto_round=True)
    burke_ratio = DecimalField(decimal_places=2, auto_round=True)
    average_month_return = DecimalField(decimal_places=2, auto_round=True)
    average_trades_month = DecimalField(decimal_places=2, auto_round=True)
    average_dd_duration = DecimalField(decimal_places=2, auto_round=True)
    trade_count = DecimalField(decimal_places=2, auto_round=True)
    alpha = DecimalField(decimal_places=2, auto_round=True)
    average_trade = DecimalField(decimal_places=2, auto_round=True)
    average_win = DecimalField(decimal_places=2, auto_round=True)
    average_loss = DecimalField(decimal_places=2, auto_round=True)
    total_wins = DecimalField(decimal_places=2, auto_round=True)
    total_losses = DecimalField(decimal_places=2, auto_round=True)
    win_rate = DecimalField(decimal_places=2, auto_round=True)
    average_mae = DecimalField(decimal_places=2, auto_round=True)
    average_mfe = DecimalField(decimal_places=2, auto_round=True)
    max_mae = DecimalField(decimal_places=2, auto_round=True)
    min_mfe = DecimalField(decimal_places=2, auto_round=True)
    ulcer_index = DecimalField(decimal_places=2, auto_round=True)
    ulcer_performance_index = DecimalField(decimal_places=2, auto_round=True)
    best_month = DecimalField(decimal_places=2, auto_round=True)
    worst_month = DecimalField(decimal_places=2, auto_round=True)
    best_day = DecimalField(decimal_places=2, auto_round=True)
    worst_day = DecimalField(decimal_places=2, auto_round=True)
    best_year = DecimalField(decimal_places=2, auto_round=True)
    worst_year = DecimalField(decimal_places=2, auto_round=True)
    average_up_month = DecimalField(decimal_places=2, auto_round=True)
    average_down_month = DecimalField(decimal_places=2, auto_round=True)
    capital_utilization = JSONField()
    rolling_sharpe = JSONField()
    returns_by_month = JSONField()
    returns_by_year = JSONField()
    percentiles = JSONField()
    drawdown_probability = JSONField()
    return_probability = JSONField()
