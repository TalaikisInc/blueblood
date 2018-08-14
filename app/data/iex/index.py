from os.path import join, dirname, abspath
from datetime import timedelta, datetime

from peewee import IntegrityError
from clint.textui import colored
from iexfinance import (Stock, get_historical_data, get_available_symbols,
    get_iex_next_day_ex_date, get_iex_corporate_actions, StockReader)
import requests_cache
from raccoon.dataframe import DataFrame

from app.db import get_exchange, Market, DB
from app.utils.vars import STORAGE_PATH


def quote(name):
    stock = Stock(name)
    return stock.get_price()

def iex_symbols():
    markets = get_available_symbols(output_format='pandas')
    e = get_exchange('IEX')
    for m in markets:
        try:
            Market.create(symbol=m['symbol'], name=m['name'],
                market_type=m['type'],
                exchange=e, enabled=m['isEnabled'])
            print(colored.green(m))
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(colored.red(err))
            DB.rollback()

def corp_actions():
    return get_iex_corporate_actions(output_format='pandas', session=session)

def dividends():
    return get_iex_dividends(output_format='pandas', session=session)

def next_day():
    return get_iex_next_day_ex_date(output_format='pandas')

def get_spread():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_effective_spread(symbols='AAPL', output_format='pandas'))

def get_company():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_company(symbols='AAPL', output_format='pandas'))

def get_financials():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_financials(symbols='AAPL', output_format='pandas'))

def get_earnings():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_earnings(symbols='AAPL', output_format='pandas'))

def get_dividends():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_dividends(symbols='AAPL', range='5y', output_format='pandas'))

def get_splits():
    s = StockReader(symbols='AAPL', output_format='pandas')
    print(s.get_splits(symbols='AAPL', range='5y', output_format='pandas'))

def run_iex():
    start_time = datetime.now() - timedelta(days=365*5)
    for n in Market.select():
        try:
            path = join(STORAGE_PATH, '{}.p'.format(n.symbol))
            data = get_historical_data(n.symbol, start=start_time, output_format='pandas')
            data.rename(columns={ 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume' }, inplace=True)
            data.to_pickle(path)
            print(colored.green(n.symbol))
        except Exception as err:
            print(colored.red(err))

def append_data(data):
    df = DataFrame(data=read_data)
    df.append(data)
