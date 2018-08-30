from os.path import abspath, join, dirname
from importlib import import_module


def run_play(model, private=True):
    if private:
        module_name = 'app.playground._private.{}'.format(model)
    else:
        module_name = 'app.playground.{}'.format(model)
    module = import_module(module_name, package='blueblood')
    module.main()
