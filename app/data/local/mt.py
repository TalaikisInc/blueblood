from os.path import join

from pandas import read_csv

from app.utils import META_PATH


def get_all_mt():
    return listdir(META_PATH)

def get_mt(symbol, period):
    df = read_csv(join(META_PATH, 'DATA_MODEL_Ava Trade EU Ltd._{}_{}.csv'.format(symbol, period)),
        skiprows=1, names=['DATE_TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'], index_col='DATE_TIME', parse_dates=[0])
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df
