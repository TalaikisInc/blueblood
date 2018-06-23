import datetime

from pandas import read_html, to_datetime


def get(params):
    if params['end_date'] is None:
        params['end_date'] = datetime.date.today().strftime("%Y%M$d")
    url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(params['symbol'], params['start_date'], params['end_date'])
    df = read_html(url)[0]
    df['Date'] = to_datetime(df['Date'])
    df = df.sort_values('Date')
    df.index = df['Date']
    del df['Date']
    df = df.rename(columns={"Open*": "Open", "Close**": "Close"})
    return df
