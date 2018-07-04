from os.path import join, dirname

from pandas import read_pickle
from fastparquet import ParquetFile


BASE_PATH = join(dirname(dirname(dirname(__file__))), 'storage')

def get_pickle(folder, name):
    return read_pickle(join(BASE_PATH, folder, '{}.p'.format(name)))

def get_parquet(name):
    apth = join(BASE_PATH, 'parq', '{}.parq'.format(name))
    pf = ParquetFile(path)
    return pf.to_pandas()
