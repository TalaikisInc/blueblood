from peewee import CharField, ForeignKeyField, DateTimeField, TextField, DecimalField

from . import BaseModel


class Source(BaseModel):
    name = CharField(unique=True)

class News(BaseModel):
    title = CharField(unique=True)
    content = TextField()
    sentiment = DecimalField(decimal_places=2, auto_round=True, default=0)
    published_date = DateTimeField()
    created_date = DateTimeField()
    source = ForeignKeyField(Source, backref='news')
    url = CharField(unique=True)
