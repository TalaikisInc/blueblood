from importlib import import_module
from os.path import dirname, join

from clint.textui import colored

from app.utils import save_indicator
from app.utils.file_utils import filenames


def generate_indicators(check_latest=True):
    fs = filenames(join(dirname(__file__), '_implementations'))

    for f in fs:
        try:
            print('Generating indicators from %s' % f)
            module_name = 'app.indicators._implementations.{}'.format(f.split('.')[0])
            imported_module = import_module(module_name, package='blueblood')
            for i in imported_module.main():
                save_indicator(i[0].dropna(), i[1], check_latest=check_latest)
                print(colored.green(i[1]))
        except Exception as err:
            print(colored.red(err))
