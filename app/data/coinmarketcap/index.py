import datetime

from pandas import read_html, to_datetime, DataFrame

from .coinmarketcappy import total_market_cap, dominance, historical_snapshots, available_snaps
from app.utils import filenames
from app.data.local import to_pickle


def get(params):
    if params['end_date'] is None:
        params['end_date'] = datetime.date.today().strftime("%Y%M$d")
    url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(params['symbol'], params['start_date'], params['end_date'])
    df = read_html(url)[0]
    df['Date'] = to_datetime(df['Date'])
    df = df.sort_values('Date')
    df.index = df['Date']
    df = df.drop(['Date'], axis=1)
    df = df.rename(columns={"Open*": "Open", "Close**": "Close"})
    return df

def _cap(date):
    snaps = historical_snapshots(date)
    df = DataFrame(snaps[date], columns=['id', 'symbol', 'name', 'cap', 'price', 'supply', 'volume'])
    to_pickle(df, 'cmc', date)

# @TODO get last available and request only after that
def get_capitalization():
    fs = filenames('cmc')
    dates = available_snaps()
    if len(fs) == 0:
        for i in range(len(dates)):
            _cap(date=dates[i])
    else:
        _cap(date=dates[0])
