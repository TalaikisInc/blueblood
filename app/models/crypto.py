from peewee import CharField, ForeignKeyField

from . import BaseModel


class CryptoExchange(BaseModel):
    title = CharField(unique=True)

class CryptoMarket(BaseModel):
    market = CharField(primary_key=True)
    exchange = ForeignKeyField(CryptoExchange, backref='markets')
