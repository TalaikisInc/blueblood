from datetime import timedelta

import requests_cache
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

from python-eodhistoricaldata import get_eod_data, get_exchanges, get_exchange_symbols, get_dividends, get_currencies, get_indexes


def exchanges():
    print(get_exchanges())

def symbols():
    for e in exchanges():
        df = get_exchange_symbols(exchange_code=e)

def run_eod():
    df = get_eod_data(symbol='AAPL', exchange='US', session=session)

def run_dividends():
    df = get_dividends(symbol, exchange)
    get_currencies()
    get_indexes()
