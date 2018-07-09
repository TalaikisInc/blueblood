from os.path import join

from fastparquet import write

from utils import STORAGE_PATH


def write_parq(df, name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    write(path, df, compression='GZIP', file_scheme='hive')
