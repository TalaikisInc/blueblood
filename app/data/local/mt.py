from os import listdir, getenv
from os.path import dirname, join, abspath, sep

from pandas import read_csv
from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(dirname(dirname(dirname(abspath(__file__))))), '.env'))

META_PATH = join(abspath(sep), "Users", "DXenu", "AppData", "Roaming", "MetaQuotes", "Terminal", getenv("META_TERMINAL_ID"), "MQL4", "Files")

def get_all():
    return listdir(META_PATH)

def get(symbol, period):
    df = read_csv(join(META_PATH, "DATA_MODEL_Ava Trade EU Ltd._{}_{}.csv".format(symbol, period)),
        skiprows=1, names=['DATE_TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'], index_col='DATE_TIME', parse_dates=[0])
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df
