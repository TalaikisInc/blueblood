from fastparquet import write

from data.local import to_pickle


def write_parq(df, name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    write(path, df, compression='GZIP', file_scheme='hive')

def to_pickle(data, folder, name):
    to_pickle(data, folder, name)
