from os.path import join

from pandas import read_csv
from urllib.request import urlretrieve

from app.data import to_pickle
from app.utils import STORAGE_PATH


def download_eurex():
    source = 'http://www.stoxx.com/download/historical_values/'
    es_url = source + 'hbrbcpe.txt'
    vs_url = source + 'h_vstoxx.txt'

    es_path = join(STORAGE_PATH, 'eurex', 'es.txt')
    vs_path = join(STORAGE_PATH, 'eurex', 'vs.txt')

    urlretrieve(es_url, es_path) # ES5
    urlretrieve(vs_url, vs_path) # VSTOXX

    columns = ['Date', 'SX5P', 'SX5E', 'SXXP', 'SXXE', 'SXXF', 'SXXA', 'DK5F', 'DKXF', 'DEL']
    es = read_csv(es_path, index_col=0, parse_dates=True, dayfirst=True, header=None, skiprows=4, names=columns, sep=';')
    del es['DEL']
    vs = read_csv(vs_path, index_col=0, parse_dates=True, dayfirst=True, header=2)

    to_pickle(es, 'eurex', 'esx')
    to_pickle(vs, 'eurex', 'vsx')
