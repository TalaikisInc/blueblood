from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader

from app.db import Index
from app.data import to_pickle

def run_stooq():
    for s in Index.select():
        data = DataReader(s.symbol, 'stooq')
        to_pickle(data, 'stooq', s.symbol)
        sleep(10)
