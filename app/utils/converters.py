from os.path import join
from os import remove

from clint.textui import colored

from .index import filenames, STORAGE_PATH
from .methods import read, write_parq
from app.data.local.mt import get_mt


def easify_names(folder='dukas'):
    fs = filenames(folder)
    for f in fs:
        try:
            splt = f.split('-')
            if len(splt) > 0:
                name = splt[0]
                oldPath = join(STORAGE_PATH, folder, f)
                path = join(STORAGE_PATH, folder, '{}.csv'.format(name))
                rename(oldPath, path)
        except Exception as err:
            print(err)

def convert_to_parq(folder='dukas'):
    fs = filenames(folder)
    for f in fs:
        name = f.split('.')[0]
        data = read(folder, name)
        write_parq(data, folder, '{}.parq'.format(name))
        remove(join(STORAGE_PATH, folder, f))
        print(colored.green(name))

def convert_mt_pickle():
    ''' Converts MT4 exported CSV to lcoal format. '''
    fs = filenames(META_PATH)
    for f in fs:
        try:
            name = f.split('_')[3]
            per = f.split('_')[4].split('.')[0]
            dest_path = join(STORAGE_PATH, 'mt', '{}_{}.p'.format(name, per))
            data = get_mt(name, per)
            if len(data) > 500:
                data.rename(columns={'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
                data.to_pickle(dest_path)
                print(colored.green('Converted for {} {}'.format(name, per)))
        except Exception as err:
            print(colored.red(err))
