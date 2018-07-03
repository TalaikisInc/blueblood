from peewee import CharField, TextField, DecimalField, ForeignKeyField

from . import BaseModel


class Address(BaseModel):
    address = CharField(primary_key=True)
    balance = DecimalField(decimal_places=2, auto_round=True, default=0)

class Contract(BaseModel):
    address = ForeignKeyField(Address, backref='contracts')
    bytecode = TextField()
    source_code = TextField()
