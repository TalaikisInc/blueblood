from time import sleep
from datetime import timedelta

from pandas_datareader import DataReader

from app.db import Market
from app.data.local import to_pickle


def run_morningstar():
    for s in Market.select():
        data = DataReader(s.symbol, 'morningstar')
        to_pickle(data, 'morningstar', s.symbol)
        sleep(10)
