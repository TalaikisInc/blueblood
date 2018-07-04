from os.path import join, dirname

from pandas import read_pickle


BASE_PATH = join(dirname(dirname(dirname(__file__))), "storage")

def get_pickle(folder, name):
    return read_pickle(join(BASE_PATH, folder, "{}.p".format(name)))
