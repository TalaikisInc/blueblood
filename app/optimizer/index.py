from pandas import concat
from numpy import where

from app.stats import stats_values
from app.data import get_pickle


def optimize(data, r, op, factor='sortino', rev=False):
    ''' Finds average of three best by give metric.'''
    df = get_pickle(folder='tiingo', name='SPY')
    market = df['SPY_AdjClose'].pct_change()
    c = concat([market, data], axis=1)
    c.columns = ['market', 'subject']
    c['ret'] = c['subject'].pct_change()

    res = []
    for i in r:
        try:
            c['func'] = c['subject'].rolling(window=i, min_periods=i).mean()
            c['action'] = where(op(c['subject'].shift(), c['func'].shift()), c['ret'], 0)
            c = c.dropna()
            r = stats_values(returns=c['action'], market=c['market'])[factor]
            res.append([i, r])
        except Exception as err:
            pass
    if len(res) > 0:
        res = sorted(res, key = lambda x: x[1], reverse=rev)
        res = [r[0] for r in res][:3]
    return sum(res) / 3.0
