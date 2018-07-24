from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader
import requests_cache

from db import Market
from app.data.local import to_pickle
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='morningstar_cache', backend='sqlite', expire_after=expire_after)


def run_morningstar():
    for s in Market.select():
        data = DataReader(s.symbol, 'morningstar', session=session)
        to_pickle(data, 'morningstar', s.symbol)
        sleep(10)
