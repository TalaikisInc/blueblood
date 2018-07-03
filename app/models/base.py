from os import getenv
from os.path import join, dirname, abspath

from peewee import PostgresqlDatabase, Model
from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(dirname(dirname(abspath(__file__)))), '.env'))

DB = PostgresqlDatabase(getenv("PG_DB"), user=getenv("PG_USER"), host=getenv("PG_SERVER"), password=getenv("PG_PASS"), port=getenv("PG_PORT"))

class BaseModel(Model):
    class Meta:
        database = DB
