from os.path import join

from pandas import read_pickle
from fastparquet import ParquetFile

from utils import STORAGE_PATH

def get_pickle(folder, name):
    return read_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))

def get_parquet(name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    pf = ParquetFile(path)
    return pf.to_pandas()
