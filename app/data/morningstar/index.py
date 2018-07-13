from os.path import join
from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader
import requests_cache

from db import Market
from utils import STORAGE_PATH
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='morningstar_cache', backend='sqlite', expire_after=expire_after)


def run_morningstar():
    for s in Market.select():
        data = DataReader(s.symbol, 'morningstar', session=session)
        data.to_pickle(join(STORAGE_PATH, 'morningstar', '{}.p'.format(s.symbol)))
        sleep(10)
