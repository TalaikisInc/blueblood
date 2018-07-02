from os.path import abspath, join, dirname
from datetime import datetime
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), "..")))

import chalk
from requests import get
from peewee import IntegrityError

from db.models.base import DB
from db.models.reddit import RedditKeyword, RedditComment
from variables.data_keywords import REDDIT_KEYWORDS

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
  try:
      RedditComment.create(
          comment_id=data["id"],
          keyword=keyword[0],
          content=data["body"],
          sentiment=0,
          created_date=datetime.fromtimestamp(data["created_utc"]))
  except IntegrityError:
      DB.rollback()
  except Exception as err:
      print(chalk.red(err))

def create(keyword, data):
    if len(data["body"]) > 100:
        key = RedditKeyword.get_or_create(keyword=keyword)
        insert(data=data, keyword=key)

def count():
    pass

def analyze():
  pass

def run():
    for keyword in REDDIT_KEYWORDS:
      for i in range(0, 365):
        s = i + 1
        part = ("{0}d".format(s), "{0}d".format(i))
        print(part)
        data = request(start_date=part[0], end_date=part[1], size=500, keyword=keyword)
        for row in data["data"]:
            create(keyword="bitcoin", data=row)

run()
