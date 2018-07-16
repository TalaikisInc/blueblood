from enum import Enum

from peewee import CharField, ForeignKeyField, IntegerField, BooleanField, TextField
from peewee_extra_fields import EnumField

from . import BaseModel


class Exchange(BaseModel):
    title = CharField(unique=True)

class TypeChoices(Enum):
    none = ''
    ad = 'American Depository Receipt (ADR\'s)',
    re = 'Real Estate Investment Trust (REIT\'s)',
    ce = 'Closed end fund (Stock and Bond Fund)',
    si = 'Secondary Issue',
    lp = 'Limited Partnerships',
    cs = 'Common Stock',
    et = 'Exchange Traded Fund (ETF)',
    fx = 'Forex',
    cfd = 'CFD'

class Market(BaseModel):
    symbol = CharField(primary_key=True)
    name = CharField()
    description = TextField(default='')
    market_type = CharField(default='')
    exchange = ForeignKeyField(Exchange, backref='markets')
    edgar_cid = IntegerField(default=0)
    enabled = BooleanField(default=True)

class Index(BaseModel):
    symbol = CharField(primary_key=True)

def get_exchange(title):
    e = Exchange.get_or_create(title=title)
    return e[0]
