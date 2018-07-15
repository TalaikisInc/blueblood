from pandas_datareader.data import DataReader

from db import Market


def run_quandl():
    for s in Market.select():
        data = DataReader(s.symbol, 'quandl')
