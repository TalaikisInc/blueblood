from os import getenv
from datetime import timedelta

try:
    from pandas_datareader import get_data_tiingo
except ImportError:
    from tiingo import TiingoClient
from requests.exceptions import HTTPError
from peewee import IntegrityError
from clint.textui import colored
from tiingo.restclient import RestClientError

from app.db import Market, DB, Source, News, get_exchange
from app.data import to_pickle


def c():
    return TiingoClient({ 'session': True, 'api_key': getenv('TIINGO_API_KEY') })

def tii_symbols():
    client = c()
    symbols = client.list_stock_tickers()
    e = get_exchange('')
    for symbol in symbols:
        try:
            meta = client.get_ticker_metadata(symbol['ticker'])
        except HTTPError as err:
            print(colored.red(err))
        except Exception as err:
            print(colored.red(err))
        if symbol['assetType'] == 'Stock':
            market_type = 'cs'
        else:
            print(symbol['assetType'])
        try:
            Market.create(symbol=symbol['ticker'], name=meta['name'], exchange=e, market_type=market_type, description=meta['description'])
            print(colored.green(symbol['ticker']))
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(colored.red(err))
            DB.rollback()

def tii_news():
    client = c()
    articles = client.get_news(tickers='GOOGL')
    for article in articles:
        source = Source.get_or_create(name=article['source'])
        News.create(title=article['title'],
            content=article['description'],
            url=article['url'],
            source=source.id,
            published_date=article['publishedDate'],
            created_date=article['crawlDate'])

def get_data(s):
    data = None
    try:
        data = get_data_tiingo(s.symbol, api_key=getenv('TIINGO_API_KEY'))
    except NameError:
        client = c()
        try:
            data = client.get_dataframe(s.symbol, startDate='1980-01-01')
            print(colored.green(s.symbol))
        except HTTPError as err:
            print(colored.red(err))
        except RestClientError as err:
            print(colored.red(err))
        except KeyError as err:
            print(colored.red(err))
    return data

def save_one(symbol):
    client = c()
    data = client.get_dataframe(symbol, startDate='1980-01-01')
    if data is not None:
        to_pickle(data, 'tiingo', '{}'.format(symbol))
    else:
        print(colored.red('Nothing for this symbols.'))

def run_tiingo(i=0):
    for s in Market.select()[i+19500:]:
        try:
            data = get_data(s=s)
            if data is not None:
                to_pickle(data, 'tiingo', '{}'.format(s.symbol))
            i += 1
        except FileNotFoundError as err:
            print(colored.red('Retrying due to disk error: {}'.format(err)))
            run_tiingo(i=i)
        except KeyError as err:
            print(colored.red(err))
