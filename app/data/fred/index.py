from os import getenv

from fredapi import Fred

from variables.data import FRED_KEYWORDS
from data.local import to_pickle
fred = Fred(api_key=getenv('FRED_API_KEY'))


def get(keyword):
    data = fred.get_series_all_releases(keyword[0])
    data.set_index('date', inplace=True)
    to_pickle(data, 'fred', keyword[0])

def run():
    for keyword in FRED_KEYWORDS:
        get(keyword=keyword)
