from datetime import timedelta

import requests_cache
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
from peewee import IntegrityError
from clint.textui import colored

from .eodhist.eod import get_eod_data, get_exchanges, get_exchange_symbols, get_dividends, get_currencies, get_indexes
from app.db import get_exchange, Market, DB
from utils import STORAGE_PATH


def exchanges():
    return get_exchanges()

def eod_symbols(e='US'):
    df = get_exchange_symbols(exchange_code=e)
    for i in range(len(df)):
        try:
            symbol = df.ix[i].name
            name = df.ix[i]['Name']
            exchange = df.ix[i]['Exchange']
            if exchange != 'NaN':
                e = get_exchange(exchange)
            else:
                e = get_exchange('')
            Market.create(symbol=symbol, name=name,
                exchange=e)
            print(colored.green(symbol))
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(colored.red(err))
            DB.rollback()

def run_eod():
    df = get_eod_data(symbol='AAPL', exchange='US', session=session)

def run_dividends():
    df = get_dividends(symbol, exchange)
    get_currencies()
    get_indexes()
