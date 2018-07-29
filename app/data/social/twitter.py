from os.path import join, dirname, abspath
from os import getenv

from clint.textui import colored
from twitter import Api


def connect():
    api = Api(consumer_key=getenv('TWITTER_KEY'), consumer_secret=getenv('TWITTER_SECRET'),
        access_token_key=getenv('TWITTER_ACCESS_TOKEN_KEY'), access_token_secret=getenv('TWITTER_ACCESS_TOKEN_SECRET'))
    return api

def get_tweets(api, handle):
    try:
        tweets = api.GetUserTimeline(screen_name=handle, exclude_replies=True, include_rts=False)
    except Exception as err:
        print(colored.red(err))
    return tweets

def get_tweets_by_tag(api, tag):
    try:
        tweets = api.GetSearch(term=tag, raw_query=None, geocode=None, since_id=None,
            max_id=None, until=None, since=None, count=50, lang='en', locale=None,
            result_type="mixed", include_entities=True)
    except Exception as err:
        print(colored.red(err))
    return tweets

def post_tweets(api, status, media):
    try:
        api.PostUpdate(status=status, media=media)
    except Exception as err:
        print(colored.red(err))
