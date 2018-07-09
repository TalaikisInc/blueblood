from os import getenv
from os.path import join

from fredapi import Fred

from variables.data import FRED_KEYWORDS
from utils import STORAGE_PATH
fred = Fred(api_key=getenv('FRED_API_KEY'))


def get(keyword):
    data = fred.get_series_all_releases(keyword[0])
    data.set_index('date', inplace=True)
    data.to_pickle(join(STORAGE_PATH, 'fred', '{0}.p'.format(keyword[0])))

def run():
    for keyword in FRED_KEYWORDS:
        get(keyword=keyword)
