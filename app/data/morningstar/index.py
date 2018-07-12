from os import getenv

from pandas_datareader import DataReader

from db import Market


def run_morningstar():
    for s in Market.select():
        data = DataReader(s.symbol, 'morningstar')
