from os import getenv
from os.path import join
from quandl import ApiConfig, get

from utils import STORAGE_PATH
from variables import QUANDL_SYMBOLS
ApiConfig.api_key = getenv('QUANDL_KEY')


def run_quandl():
    for s in QUANDL_SYMBOLS:
        data = get(s)
        name = s.replace('/', '_')
        data.to_pickle(join(STORAGE_PATH, 'futures', '{}.p'.format(name)))
