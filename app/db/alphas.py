from peewee import CharField
from peewee_extra_fields import EnumField

from . import BaseModel


class AlphaOwner(BaseModel):
    name = CharField()
    email = CharField()

    class Meta:
        indexes = (
            (('name', 'email'), True),
        )
