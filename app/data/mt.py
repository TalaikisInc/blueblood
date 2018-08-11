from os.path import join

from pandas import read_csv

from app.utils import META_PATHS


def get_all_mt():
    lst = []
    for m in META_PATHS:
        lst.append(listdir(m))
    return lst

def get_mt(f, which=0):
    df = read_csv(join(META_PATHS[which], f),
        skiprows=1, names=['DATE_TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'], index_col='DATE_TIME', parse_dates=[0])
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df
