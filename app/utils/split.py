from os.path import join
from os import remove

from app.data.local import get_csv
from app.utils import STORAGE_PATH
from .index import filenames, STORAGE_PATH


def train_test_split(data, part=0.7):
    ''' Splits data into tain and test sets. '''
    train = data.iloc[:int(len(data.index)*part)]
    test = data.iloc[int(len(data.index)*part):]
    return (train, test)

def split_ticks(folder, symbol):
    ''' Splits big file into chunks. '''
    for i, chunk in enumerate(get_csv(folder=folder, name=symbol, skip=True)):
        chunk.to_csv(join(STORAGE_PATH, folder, '_split', '{}_{}.csv'.format(name, i))

def count_splits(folder):
    ''' Counts total split files in _splits of the directory. '''
    return len(filenames(join(folder, '_split')))

def clean_splits(folder):
    ''' Cleans split files in _splits of the directory. '''
    path = join(folder, '_split')
    fs = filenames(path)
    for f in fs:
        remove(join(STORAGE_PATH, path, f))
