from matplotlib import pyplot as plt
from numpy import where

from data.local import get_pickle, join_data, transform_multi_data
from utils import train_test_split
from models.alpha import alpha, all_alphas
from stats import commissions

def comm(q, p=0.01):
    return abs(q) * p

def quantity(capital, price, alloc):
    return capital / price * alloc

"""
def res(s, data):
    test = Backtest(s, data, commissions=commissions)
    res = run(test)
    res.display()
    res.plot()
    plt.show()
    # #TODO add MAE< MFE
    # @TODO add more stats
"""

def diff(data, symbols):
    for s in symbols:
        data['{}_Diff'.format(s)] = data['{}_Close'.format(s)].diff()
    return data

def clean(data, symbols):
    for s in symbols:
        data.drop(['{}_Open'.format(s),
            '{}_High'.format(s),
            '{}_Low'.format(s),
            '{}_Close'.format(s),
            '{}_Volume'.format(s)
        ], axis=1)
    return data

def basic_runs():
    # should be moved into collections:
    SYMBOLS = ['SP500_1440', 'NASDAQ100_1440', 'RUSSELL2000_1440', 'DAX30_1440',
        'FTSE100_1440', 'DJ30_1440', '10YTNOTES_1440', 'GOLD_1440', 'OMX30_1440',
        'NIFTY50_1440', 'CAC40_1440']
    initial = get_pickle('mt', SYMBOLS[0])
    initial = transform_multi_data(data=initial, symbol='SP500_1440')
    initial = join_data(primary=initial, folder='mt', symbols=SYMBOLS[1:])
    data, test = train_test_split(data=initial.dropna(), part=0.6)

    for i in all_alphas():
        print(i)
        a = alpha(model=i, data=data, symbols=SYMBOLS).fillna(0.0)
        a = diff(data=a, symbols=SYMBOLS)
        # a = clean_transform(data=a, symbols=SYMBOLS)
        # should be moved into rebalancing, allocations, weights, etc.
        for s in SYMBOLS:
            q = quantity(capital=10000, price=a['{}_Open'.format(s)], alloc=1.0)
            # move to rule book
            a['{}_Shifted'.format(s)] = a[s].shift()
            a['{}_Sig'.format(s)] = where(a['{}_Shifted'.format(s)] > 8, 1, 0)
            a['{}_Comm'.format(s)] = commissions(signals=a['{}_Sig'.format(s)], com=comm(q=q))
            a['{}_Ret'.format(s)] = where(a['{}_Sig'.format(s)] == 1, a['{}_Diff'.format(s)] - a['{}_Comm'.format(s)], 0)
            # do stats
            plt.plot(a['{}_Ret'.format(s)].cumsum())
            plt.show()
