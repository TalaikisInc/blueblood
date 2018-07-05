from datetime import datetime

from iexfinance import Stock, get_historical_data, get_available_symbols,
    get_corporate_actions, get_dividends, get_iex_next_day_ex_date
import requests_cache

expiry = datetime.timedelta(days=1)
session = requests_cache.CachedSession(cache_name='iex_cache', backend='sqlite', expire_after=expiry)

def quote(name):
    stock = Stock(name)
    return stock.get_price()

def symbols():
    return get_available_symbols(output_format='pandas', session=session)

def corp_actions():
    return get_corporate_actions(output_format='pandas', session=session)

def dividends():
    return get_dividends(output_format='pandas', session=session)

def next_day():
    return get_iex_next_day_ex_date(output_format='pandas')

def history(name, s=(2017, 2, 9), e=(2018, 2, 9)):
    start = datetime(s)
    end = datetime(e)

    return get_historical_data(name, start=start, end=end, output_format='pandas', session=session)
