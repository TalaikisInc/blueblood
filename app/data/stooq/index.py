from os.path import join
from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader
import requests_cache

from db import Index
from utils import STORAGE_PATH
expire_after = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='stooq_cache', backend='sqlite', expire_after=expire_after)

def run_stooq():
    for s in Index.select():
        data = DataReader(s.symbol, 'stooq')
        data.to_pickle(join(STORAGE_PATH, 'stooq', '{}.p'.format(s.symbol)))
        sleep(10)
