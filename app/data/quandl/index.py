from os import getenv
from quandl import ApiConfig, get
from clint.textui import colored

from app.data import to_pickle
from app.variables import QUANDL_SYMBOLS
ApiConfig.api_key = getenv('QUANDL_KEY')
from app.utils import ensure_latest


def run_quandl():
    for s in QUANDL_SYMBOLS:
        data = get(s[0])
        name = s[0].replace('/', '_')
        if s[2]:
            ensure_latest(df=data)
        to_pickle(data, 'futures', name)
        print(colored.green(name))
