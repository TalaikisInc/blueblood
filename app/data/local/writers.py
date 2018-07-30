from os.path import join

from fastparquet import write

from app.utils.index import STORAGE_PATH


def write_parq(df, name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    write(path, df, compression='GZIP', file_scheme='hive')

def to_pickle(data, folder, name):
    data.to_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))
