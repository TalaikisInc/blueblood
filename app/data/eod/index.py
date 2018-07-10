from datetime import timedelta
from os.path import join

import requests_cache
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
from peewee import IntegrityError
from clint.textui import colored

from .eodhist.eod import get_eod_data, get_exchanges, get_exchange_symbols, get_dividends, get_currencies, get_indexes
from app.db import get_exchange, Exchange, Market, DB
from utils import STORAGE_PATH


def exchanges():
    return get_exchanges()

def eod_symbols(e='US'):
    df = get_exchange_symbols(exchange_code=e, session=session)
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
    for n in Market.select():
        try:
            exchanges = ['NASDAQ', 'NYSE']
            e = Exchange.get(id=n.exchange)
            if any(e for e in exchanges):
                path = join(STORAGE_PATH, 'eod', '{}.p'.format(n.symbol))
                df = get_eod_data(symbol=n.symbol, exchange='US')
                if len(df) > 100:
                    df.to_pickle(path)
                    print(colored.green(n.symbol))
        except Exception as err:
            print(colored.red(err))

def run_dividends():
    df = get_dividends(symbol, exchange)
    get_currencies()
    get_indexes()
