from peewee import CharField, ForeignKeyField, DateTimeField, TextField, DecimalField, IntegerField

from . import BaseModel


class RedditKeyword(BaseModel):
    keyword = CharField(unique=True)

class RedditComment(BaseModel):
    comment_id = CharField(primary_key=True)
    keyword = ForeignKeyField(RedditKeyword, backref='keywords')
    content = TextField()
    sentiment = DecimalField(decimal_places=2, auto_round=True, default=0)
    created_date = DateTimeField()

class RedditCommentCount(BaseModel):
    date = DateTimeField(unique=True)
    keyword = ForeignKeyField(RedditKeyword, backref='keywords')
    count = IntegerField()
