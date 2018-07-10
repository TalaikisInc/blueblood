from os.path import join

from clint.textui import colored
from pandas import read_pickle
from fastparquet import ParquetFile

from app.utils import STORAGE_PATH
from .mt import get_mt, META_PATH
from utils import filenames


def get_pickle(folder, name):
    return read_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))

def get_parquet(name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    pf = ParquetFile(path)
    return pf.to_pandas()

def fill_forward(data):
    return data.fillna(method='ffill')

def clean(folder, data):
    if folder == 'fred':
        del data['realtime_start']
    if folder == 'mt':
        del data['Open']
        del data['High']
        del data['Low']
        del data['Volume']
    return data

def join_data(primary, folder, factors):
    i = 0
    for factor in factors:
        data = get_pickle(folder, factor)
        data = clean(folder=folder, data=data)
        data.columns = [factors[i]]
        primary = primary.join(data, how='left')
        i = i + 1
    return fill_forward(data=primary)

def convert_mt_pickle():
    fs = filenames(path=META_PATH)
    for f in fs:
        try:
            name = f.split('_')[3]
            per = f.split('_')[4].split('.')[0]
            dest_path = join(STORAGE_PATH, 'mt', '{}_{}.p'.format(name, per))
            data = get_mt(name, per)
            if len(data) > 100:
                data.rename(columns={'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
                data.to_pickle(dest_path)
                print(colored.green('Converted for {} {}'.format(name, per)))
        except Exception as err:
            print(colored.red(err))
