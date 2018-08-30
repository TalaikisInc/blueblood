from importlib import import_module
from os.path import dirname, join

from clint.textui import colored

from app.utils.file_utils import filenames


def run_watchdogs():
    fs = filenames(join(dirname(__file__), '_implementations'), resampled=True)
    fs += filenames(join(dirname(__file__), '_implementations'), resampled=False)

    for f in fs:
        print('Generating watcher %s' % f)
        try:
            module_name = 'app.watchdogs._implementations.{}'.format(f.split('.')[0])
            imported_module = import_module(module_name, package='blueblood')
            imported_module.main()
        except Exception as err:
            print(colored.red(err))
