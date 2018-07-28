from os import getenv

from fredapi import Fred

from app.variables.data import FRED_KEYWORDS
from app.data.local import to_pickle
fred = Fred(api_key=getenv('FRED_API_KEY'))


def get(keyword):
    data = fred.get_series_all_releases(keyword[0])
    data.set_index('date', inplace=True)
    to_pickle(data, 'fred', keyword[0])

def run_fred():
    for keyword in FRED_KEYWORDS:
        get(keyword=keyword)
