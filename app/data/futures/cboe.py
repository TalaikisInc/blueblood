from os.path import join
from io import StringIO

from pandas import read_csv, to_datetime
from requests import get

from app.utils import STORAGE_PATH
from variables import CBOE_DATA


def cboe_download():
    for sym in CBOE_DATA:
        url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/%s.csv' % sym[1]
        path = join(STORAGE_PATH, sym[0])
        content = get(url).content
        data = read_csv(StringIO(content.decode('utf-8')), skiprows=3, names=sym[2], parse_dates=True)
        data.index = to_datetime(data['Date'])
        del data['Date']
        data.to_pickle(path)
