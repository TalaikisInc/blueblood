from os.path import join, dirname

from fastparquet import write


BASE_PATH = join(dirname(dirname(dirname(__file__))), 'storage')

def write_parq(df, name):
    path = join(BASE_PATH, 'parq', '{}.parq'.format(name))
    write(path, df, compression='GZIP', file_scheme='hive')
