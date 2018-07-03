from os import getenv
from os.path import join, dirname, abspath
from os.path import abspath, join, dirname
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), "../..")))

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(dirname(dirname(dirname(abspath(__file__))))), '.env'))
from fredapi import Fred

from variables.data import FRED_KEYWORDS


fred = Fred(api_key=getenv("FRED_API_KEY"))
base_path = join(dirname(dirname(dirname(abspath(__file__)))), "storage", "fred")

def get(keyword):
    data = fred.get_series_all_releases(keyword[0])
    data.set_index('date', inplace=True)
    data.to_pickle(join(base_path, "{0}.p".format(keyword[0])))

def run():
    for keyword in FRED_KEYWORDS:
        get(keyword=keyword)

run()
