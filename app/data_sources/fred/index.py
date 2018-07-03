from os import getenv
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(dirname(dirname(abspath(__file__)))), '.env'))
from fredapi import Fred

from variables.data_keywords import FRED_KEYWORDS

fred = Fred(api_key=getenv("FRED_API_KEY"))

def get(keyword):
    data = fred.get_series_all_releases(keyword)