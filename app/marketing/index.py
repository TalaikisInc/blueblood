from os.path import (isfile, join)
from datetime import date

from django.conf import settings

from clint.textui import colored
import twitter

from .models import (Signals, QtraUser, Brokers)


def connect():
    api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY, \
          consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET, \
          access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY, \
          access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

    return api


def get_tweets(handle):
    try:
        tweets = api.GetUserTimeline(screen_name=handle, exclude_replies=True, \
                    include_rts=False)  # includes entities
        return tweets
    except:
        return None


def get_tweets_by_tag(tag):
    try:
        tweets = api.GetSearch(term=tag, raw_query=None, geocode=None, since_id=None, \
                    max_id=None, until=None, since=None, count=50, lang='en', locale=None, \
                    result_type="mixed", include_entities=True)
        return tweets
    except:
        return None


def signal_poster(api, signal, strings):
    try:
        returns = signal.returns

        if returns > 0:
            returns_string = "won"
        elif returns < 0:
            returns_string = "lost"
        else:
            returns_string = None

        if not (returns_string is None):
            status = "{0} {1} signal ({2}) for #{3} {4} ${5}: https://quantrade.co.uk/{6}/{7}/{8}/{9}/{10}/  #trading #signals".format(signal.date_time.strftime('%d, %b %Y'), strings[0], \
                signal.system.title, signal.symbol.symbol, returns_string, returns, \
                signal.broker.slug, signal.symbol.symbol, signal.period.period, \
                signal.system.title, strings[1])

            media = "https://quantrade.co.uk/static/collector/images/meta/{0}=={1}=={2}=={3}=={4}.png".format(\
                signal.broker.slug, signal.symbol.symbol, signal.period.period, signal.system.title, strings[1])

            print("Twitter status: {0}".format(status))
            print("Media: {0}".format(media))

            filename = join(settings.STATIC_ROOT, 'collector', 'images', 'meta', media.split('meta/')[1])

            if isfile(filename):
                api.PostUpdate(status=status, media=media)
            else:
                api.PostUpdate(status=status, media=None)

            print(colored.green("Sent tweet."))
            signal.posted_to_twitter = True
            signal.save()
    except Exception as err:
        print(colored.red("Twitter signal poster".format(err)))


def post_tweets():
    try:
        api = connect()

        signals = Signals.objects.filter(posted_to_twitter=False).exclude(returns__isnull=True)

        for signal in signals:
            try:
                if signal.returns != 0:

                    if signal.direction == 1:
                        signal_poster(api=api, signal=signal, strings=['Buy', 'longs'])
                    elif signal.direction == 2:
                        signal_poster(api=api, signal=signal, strings=['Sell', 'shorts'])

            except Exception as e:
                print(e)
                continue

    except Exception as e:
        print(colored.red("At Twitter posting: {0}".format(e)))


def heatmap_to_twitter():
    try:
        now = date.today()
        d = now.day

        if d == 2:
            api = connect()
            for broker in Brokers.objects.all():
                image_filename = join(settings.STATIC_ROOT, 'collector', 'images', \
                    'heatmap', '{0}=={1}=={2}=={3}=={4}.png'.format(broker.slug, \
                    'AI50', '1440', 'AI50', 'longs'))

                if isfile(image_filename):
                    media = "https://quantrade.co.uk/static/collector/images/heatmap/{0}=={1}=={2}=={3}=={4}.png".\
                        format(broker.slug, 'AI50', '1440', 'AI50', 'longs')
                else:
                    media = None

                status = "Results including last month index performance for {}.".format(broker.title)

                api.PostUpdate(status=status, media=media)
                print(colored.green("Heatmap posted."))
    except Exception as e:
        print(colored.red("At heatmap_to_twitter {}".format(e)))
