from os.path import join
import gzip
from datetime import datetime

from requests import get

from utils import STORAGE_PATH, filenames


# #TODO examine available data and download only missing/ latest
def run_fxcm():
    symbols = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'CADCHF', 'EURAUD', 'EURCHF', 'EURGBP',
        'EURJPY', 'EURUSD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY',
        'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY', 'AUDUSD', 'CADJPY', 'GBPCAD', 'USDTRY', 'EURNZD']
    end = datetime.now()
    end_week = end.isocalendar()[1]

    for symbol in symbols:
        for year in range(2015, end.year):
            for w in range(1, 53):
                if not ((end.year == year) & (w == end_week)):
                    url = 'https://tickdata.fxcorporate.com/{}/{}/{}.csv.gz'.format(symbol, year, w)
                    data = get(url)
                    file_name = join(STORAGE_PATH, 'fxcm', '{}_{}_{}.gz'.format(symbol, year, w))
                    with open(file_name, 'wb') as f:
                        f.write(data.content)

def decompress():
    fs = filenames('fxcm')
    for filename in fs:
        if '.gz' in filename:
            with gzip.open(join(STORAGE_PATH, 'fxcm', filename), 'rb') as f:
                content = f.read()
                print(gzip.decompress(content))
