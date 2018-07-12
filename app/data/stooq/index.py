from os import getenv

from pandas_datareader import DataReader

from db import Index


def run_stooq():
    for s in Index.select():
        data = DataReader(s.symbol, 'stooq')
