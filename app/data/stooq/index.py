from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader
import requests_cache

from db import Index
from app.data.local import to_pickle
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='stooq_cache', backend='sqlite', expire_after=expire_after)

def run_stooq():
    for s in Index.select():
        data = DataReader(s.symbol, 'stooq')
        to_pickle(data, 'stooq', s.symbol)
        sleep(10)
