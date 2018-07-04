from os.path import join, dirname

from pandas import read_pickle


BASE_PATH = join(dirname(dirname(__file__)), "storage")

def get_pickle(folder, name):
    return read_pickle(join(NASE_DIR, folder, "{}.p".format(name)))
