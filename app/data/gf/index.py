from time import sleep
from datetime import timedelta

from pandas_datareader.data import DataReader

from app.db import Market
from app.data.local import to_pickle


def run_gf():
    for s in Market.select():
        data = DataReader(s.symbol, 'google')
        to_pickle(data, 'gf', s.symbol)
        sleep(10)
