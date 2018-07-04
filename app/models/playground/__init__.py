from importlib import import_module


def run_play(model):
    #import_module('.{}'.format(model))
    module_name = 'app.models.playground.{}'.format(model)
    special_module = import_module(module_name, package='blueblood')
