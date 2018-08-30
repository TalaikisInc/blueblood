from os.path import join

from fastparquet import write

from app.utils.vars import STORAGE_PATH


def write_parq(df, name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    write(path, df, compression='GZIP', file_scheme='hive')

def to_pickle(data, folder, name):
    ''' Saves pandasDataFrame to pickle.'''
    data.to_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))
