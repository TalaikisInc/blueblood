from os.path import abspath, join, dirname
from datetime import datetime
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), "..")))

import chalk
from requests import get
from peewee import IntegrityError

from db.models.reddit import RedditKeyword, RedditComment

def request(start_date, end_date, size, keyword):
    payload = {
        'q': keyword,
        'size': size,
        'after': start_date,
        'before': end_date
      }
    r = get("https://apiv2.pushshift.io/reddit/search/comment/", params=payload)
    return r.json()

def insert(data, keyword):
  RedditComment.create(
      comment_id=data["id"],
      keyword=keyword[0],
      content=data["body"],
      sentiment=0,
      created_date=datetime.fromtimestamp(data["created_utc"]))

def create(keyword, data):
    try:
        if len(data["body"]) > 100:
            key = RedditKeyword.get_or_create(keyword=keyword)
            insert(data=data, keyword=key)
    except IntegrityError:
      pass
    except Exception as err:
      print(chalk.red(err))

def count():
    pass

def analyze():
  pass

def run():
    keywords = ["hodl"]
    parts = [
      ("365d", "335d"),
      ("335d", "305d"),
      ("305d", "275d"),
      ("275d", "245d"),
      ("245d", "215d"),
      ("215d", "175d"),
      ("175d", "145d"),
      ("115d", "85d"),
      ("85d", "55d"),
      ("55d", "25d"),
      ("25d", "0d")
      ]
    for keyword in keywords:
      for part in parts:
        data = request(start_date=part[0], end_date=part[1], size=500, keyword=keyword)
        for row in data["data"]:
            print(row)
            create(keyword="bitcoin", data=row)

run()
