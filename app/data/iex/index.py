from datetime import timedelta, datetime
from sys import exit

from peewee import IntegrityError
from clint.textui import colored
from iexfinance import Stock, get_historical_data, get_available_symbols, get_iex_next_day_ex_date
import requests_cache

expiry = timedelta(days=1)
session = requests_cache.CachedSession(cache_name='iex_cache', backend='sqlite', expire_after=expiry)
from app.db import get_exchange, Market
from app.db import DB


def quote(name):
    stock = Stock(name)
    return stock.get_price()

def run_symbols():
    markets = get_available_symbols(output_format='pandas', session=session)
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
    return get_corporate_actions(output_format='pandas', session=session)

def dividends():
    return get_dividends(output_format='pandas', session=session)

def next_day():
    return get_iex_next_day_ex_date(output_format='pandas')

def run_history(name):
    now = datetime.now()
    for year in range(2000, now.year):
        if year == now.year:
            end_month = now.month
        else:
            end_month = 12
        for month in range(1, end_month):
            if month == end_month:
                end_day = now.day
            else:
                end_day = 31
            for day in range(1, end_day):
                try:
                    start = datetime(year, month, day)
                    end = datetime(year, month, day)
                    print(get_historical_data(name, start=start, end=end, output_format='pandas', session=session))
                except:
                    exit(1)
    
    return True
