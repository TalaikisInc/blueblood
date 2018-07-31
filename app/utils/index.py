from os import listdir, chdir, makedirs, rename
from os.path import isfile, join, abspath, exists
from collections import namedtuple

from numba import jit
from numpy import log, cumsum, log2, nonzero, sum, histogram2d, sqrt, polyfit, subtract, std
from numpy.polynomial import Polynomial
from pandas import DataFrame, Series
from peewee import Field
from sklearn.metrics import mutual_info_score, log_loss
from statsmodels.api import OLS
from pyfinance.ols import PandasRollingOLS
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from matplotlib import pyplot as plt


STORAGE_PATH = abspath(chdir('G:\\storage'))
DATA_SOURCE = 'eod'

def peewee_to_df(table):
    fields = [f for f in dir(table) if isinstance(getattr(table, f), Field)]
    data = list(table.select(*[getattr(table, fld) for fld in fields]).tuples())
    df = DataFrame.from_records(data, columns=table._meta.fields)

    if 'id' in fields:
        df.set_index('id', inplace=True)
    return df

def periodize_returns(r, p=252):
    return ((1 + r) ^ p - 1)

def filenames(folder):
    try:
        path = join(STORAGE_PATH, folder)
        fs = [f for f in listdir(path) if isfile(join(path, f)) & ('.gitkeep' not in f)]
    except:
        path = folder
        fs = [f for f in listdir(path) if isfile(join(path, f))]
    return fs

def log_returns(x):
    return log(x)

def get_dividends_splits(close, adjusted):
    '''Outputs should be classified into: dividend, split or white noise.'''
    return adjusted - close

@jit
def vwap(v, h, l):
    return cumsum(v * (h + l) / 2) / cumsum(v)

def shanon_entropy(c):
    norm = c / float(sum(c))
    norm = norm[nonzero(norm)]
    H = -sum(norm * log2(norm))  
    return H

def mutual_info(x, y, bins):
    c_xy = histogram2d(x, y, bins)[0]
    return mutual_info_score(None, None, contingency=c_xy)

def logloss(prtedicted, y, name):
    val = log_loss(y, predicted)
    print('Log Loss for {}: {:.6f}.'.format(name, val))
    return val

def diff(data, symbols, d_type='accepted'):
    if d_type == 'accepted':
        for s in symbols:
            data['{}_Diff'.format(s)] = data['{}_AdjClose'.format(s)].diff()
    elif d_type == 'eod':
        for s in symbols:
            data['{}_Diff'.format(s)] = data['{}_Adjusted_close'.format(s)].diff()
    else:
        for s in symbols:
            data['{}_Diff'.format(s)] = None
    return data

def pct(data, symbols, d_type='accepted'):
    if d_type == 'accepted':
        for s in symbols:
            data['{}_Pct'.format(s)] = data['{}_AdjClose'.format(s)].pct_change()
    elif d_type == 'eod':
        for s in symbols:
            data['{}_Pct'.format(s)] = data['{}_Adjusted_close'.format(s)].pct_change()
    else:
        for s in symbols:
            data['{}_Pct'.format(s)] = None
    return data

def zscore(data, per):
    return (data - data.rolling(window=per, min_periods=per).mean()) / data.rolling(window=per, min_periods=per).std()

def minmaxscaler(data, per):
    return (data - data.rolling(window=per, min_periods=per).min()) / (data.rolling(window=per, min_periods=per).max() - data.rolling(window=per, min_periods=per).min())

def slope(data0, data1):
    return OLS(data1, data0).fit().params[0]

def roll_slope(data0, data1, per):
    return PandasRollingOLS(y=data1, x=data0, window=per).beta

def compound_interest(principal, rate, years):
    ''' Compound interest. '''
    for _ in range(years):
        principal *= rate
    return round(principal, 2)

def parkinson_vol(close, per):
    ''' Parkinsons' volatility. '''
    var = (close - close.rolling(window=per, min_periods=per).mean())
    var2 = var * var
    return sqrt(var2.rolling(window=(per-1), min_periods=(per-1)).sum() * 1/(4*log(2)) * 252/(per-1))

def hurst(ts):
    ''' Returns the Hurst Exponent. '''
    lags = range(2, 20)
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = polyfit(log(lags), log(tau), 1)
    return poly[0] * 2.0

def poly(x, y, plot=False):
    p = Polynomial.fit(y, x, 3)
    if plot:
        plt.scatter(x, y)
        plt.plot(*p.linspace(), lw=3, color='r')
        plt.show()
    return p

def rank(array):
    s = Series(array)
    return s.rank(ascending=False)[len(s)-1]

Pair = namedtuple('Pair', 'symbol_a symbol_b')
Owner = namedtuple('Owner', 'name email')
Fixed = namedtuple('Fixed', 'symbol')
LongRule = namedtuple('LongRule', 'op value')
ShortRule = namedtuple('ShortRule', 'op value')

def makedir(f):
    path = join(STORAGE_PATH, f)
    if not exists(path):
        makedirs(path)

def if_exists(folder, name):
    return exists(join(STORAGE_PATH, folder, '{}.p'.format(name)))

def common(fs1, fs2):
    return set.intersection(*map(set, [fs1, fs2]))

def corrwith(data, benchmark):
    return data.drop(benchmark, 1).corrwith(data[benchmark])
    
def count_zeros(df, col):
    df[col] = df[col].loc[df[col] == 0]
    z = len(df[col])
    if z != 0:
        return len(df[col]) / z
    else:
        return 0

def avg_spread(df):
    return (df['Ask'] - df['Bid']).mean()

def comm(q, p=0.01):
    return abs(q) * p

def quantity(capital, price, alloc):
    return capital / price * alloc
