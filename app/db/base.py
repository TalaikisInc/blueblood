from os import getenv

from peewee import PostgresqlDatabase, Model

DB = PostgresqlDatabase(getenv("PG_DB"), user=getenv("PG_USER"), host=getenv("PG_SERVER"), password=getenv("PG_PASS"), port=getenv("PG_PORT"))


class BaseModel(Model):
    class Meta:
        database = DB
