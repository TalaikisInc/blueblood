from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from pandas.tseries.offsets import Week


def ensure_latest(df, symbol=None):
    latest = df.tail(1).index.strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    ago2 = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    ago3 = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    dow = datetime.today().weekday()
    if (dow == 6) | (dow == 0):
        acceptable = [ago3, ago2]
    else:
        acceptable = [ago2, yesterday, today]
    if symbol is not None:
        assert latest in acceptable, '[%s] Data isn\'t latest! Expected any of %s, got %s' % (symbol, acceptable, latest)
    else:
        assert latest in acceptable, 'Data isn\'t latest! Expected any of %s, got %s' % (acceptable, latest)        

def vx_expiry(year, month):
    t = datetime(year, month, 1) + relativedelta(months=1)
    offset = Week(weekday=4)
    if t.weekday() != 4:
        t_new = t + 3 * offset
    else:
        t_new = t + 2 * offset
    t_exp = t_new - timedelta(days=30)
    return t_exp
