from peewee import IntegerField
from playhouse.postgres_ext import JSONField

from . import BaseModel


class Block(BaseModel):
    block_id = IntegerField()
    data = JSONField()