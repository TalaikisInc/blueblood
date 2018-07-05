from peewee import CharField, ForeignKeyField, IntegerField

from . import BaseModel


class Exchange(BaseModel):
    title = CharField(unique=True)

class MarketType(BaseModel):
    title = CharField(unique=True)

class Market(BaseModel):
    market = CharField(primary_key=True)
    market_type = ForeignKeyField(MarketType, backref='market_type')
    exchange = ForeignKeyField(Exchange, backref='markets')
    edgar_cid = IntegerField(default=0)
