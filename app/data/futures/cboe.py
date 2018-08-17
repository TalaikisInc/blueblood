from io import StringIO

from pandas import to_datetime, read_csv
from requests import get
from clint.textui import colored

from app.variables import CBOE_DATA
from app.data import to_pickle
from app.utils import ensure_latest


def cboe_download():
    for sym in CBOE_DATA:
        url = 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/%s.csv' % sym[1]
        content = get(url).content
        data = read_csv(StringIO(content.decode('utf-8')), skiprows=4, names=sym[2], parse_dates=True)
        data.index = to_datetime(data['Date'], errors='coerce')
        del data['Date']
        ensure_latest(df=data)
        to_pickle(data, 'indicators', sym[0])
        print(colored.green(sym[0]))
