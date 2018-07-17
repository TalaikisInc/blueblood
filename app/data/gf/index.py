from time import sleep
from datetime import timedelta

import requests_cache
from pandas_datareader.data import DataReader

from db import Market
from data.lcoal import to_pickle
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='gf_cache', backend='sqlite', expire_after=expire_after)


def run_gf():
    for s in Market.select():
        data = DataReader(s.symbol, 'google', session=session)
        to_pickle(data, 'gf', s.symbol)
        sleep(10)
