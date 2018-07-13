from os import getenv
from os.path import join
from datetime import timedelta

try:
    from pandas_datareader import get_data_tiingo
except ImportError:
    from tiingo import TiingoClient
import requests_cache
from requests.exceptions import HTTPError
from peewee import IntegrityError
from clint.textui import colored
from tiingo.restclient import RestClientError

from db import Market, DB, Source, News
from utils import STORAGE_PATH
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='stooq_cache', backend='sqlite', expire_after=expire_after)


def c():
    return TiingoClient({ 'session': True, 'api_key': getenv('TIINGO_API_KEY') })

def tii_symbols():
    client = c()
    symbols = client.list_stock_tickers()
    for symbol in symbols:
        try:
            meta = client.get_ticker_metadata(symbol['ticker'])
            # @TODO Add to db
            # meta['description']
        except HTTPError as err:
            print(colored.red(err))
        if symbol['assetType'] == 'Stock':
            market_type = 'cs'
        else:
            print(symbol['assetType'])
        try:
            Market.create(symbol=symbol['ticker'], name=meta['name'], exchange=0, market_type=market_type)
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

def run_tiingo():
    for s in Market.select():
        try:
            data = get_data_tiingo(s.symbol, api_key=getenv('TIINGO_API_KEY'), session=session)
        except NameError:
            client = c()
            try:
                data = client.get_dataframe(s.symbol, startDate='1980-01-01')
                print(colored.green(s.symbol))
            except HTTPError as err:
                print(colored.red(err))
            except RestClientError as err:
                print(colored.red(err))
        data.to_pickle(join(STORAGE_PATH, 'tiingo', '{}.p'.format(s.symbol)))
