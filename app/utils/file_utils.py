from os.path import join, isfile, exists
from os import listdir, remove, makedirs

from clint.textui import colored

from .vars import STORAGE_PATH


def filenames(folder, resampled=False, mt=False):
    try:
        if mt:
            fs = [f for f in listdir(folder) if isfile(join(folder, f)) if 'DATA_MODEL' in f]
        else:
            path = join(STORAGE_PATH, folder)
            fs = [f for f in listdir(path) if isfile(join(path, f)) & ('.gitkeep' not in f)]
            if not resampled:
                fs = [i for i in fs if ('_' not in i) & ('.gitkeep' not in i)]
            else:
                fs = [i for i in fs if ('_' in i) & ('.gitkeep' not in i)]
    except:
        path = folder
        fs = [f for f in listdir(path) if isfile(join(path, f))]
    return fs

def clean_storage():
    folders = ['portfolios', 'indicators', 'strategies']
    for folder in folders:
        fs = filenames(folder)
        for f in fs:
            remove(join(STORAGE_PATH, folder, f))
            print(colored.green('Removed %s ' % f))

def makedir(f):
    path = join(STORAGE_PATH, f)
    if not exists(path):
        makedirs(path)

def if_exists(folder, name):
    return exists(join(STORAGE_PATH, folder, '{}.p'.format(name)))
