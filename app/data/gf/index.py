from time import sleep
from os.path import join

from pandas_datareader.data import DataReader

from db import Market
from utils import STORAGE_PATH


def run_gf():
    for s in Market.select():
        data = DataReader(s.symbol, 'google')
        data.to_pickle(join(STORAGE_PATH, 'gf', '{}.p'.format(s.symbol)))
        sleep(10)
