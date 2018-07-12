from os import getenv

from pandas_datareader import get_data_tiingo

from db import Market


def run_tiingo():
    for s in Market.select():
        data = get_data_tiingo(s.symbol, api_key=getenv('TIINGO_API_KEY'))
