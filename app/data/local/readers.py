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

def transform_multi_data(data, symbol):
    for col in data.columns:
        data['{}_{}'.format(symbol, col)] = data[col]
        del data[col]
    return data

def clean(folder, data):
    if folder == 'fred':
        data = data.drop(['realtime_start'], axis=1)
    if folder == 'eod':
        data = data.drop(['Open', 'High', 'Low', 'Volume', 'Adjusted_close'], axis=1)
    return data

def join_data(primary, folder, symbols, clr=False):
    for symbol in symbols:
        data = get_pickle(folder, symbol).dropna()
        if clr:
            data = clean(folder=folder, data=data)
        data = transform_multi_data(data=data, symbol=symbol)
        primary = primary.join(data, how='left')
    return fill_forward(data=primary)

def convert_mt_pickle():
    fs = filenames(path=META_PATH)
    for f in fs:
        try:
            name = f.split('_')[3]
            per = f.split('_')[4].split('.')[0]
            dest_path = join(STORAGE_PATH, 'mt', '{}_{}.p'.format(name, per))
            data = get_mt(name, per)
            if len(data) > 1000:
                data = data.rename(columns={'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
                data.to_pickle(dest_path)
                print(colored.green('Converted for {} {}'.format(name, per)))
        except Exception as err:
            print(colored.red(err))
