from os import listdir, chdir, makedirs, rename, getenv
from os.path import isfile, join, abspath, exists
from collections import namedtuple

from numba import jit
from numpy import log, cumsum, log2, nonzero, sum, histogram2d, sqrt, polyfit, subtract, std
from numpy.polynomial import Polynomial
from pandas import DataFrame, Series
from peewee import Field
from sklearn.metrics import mutual_info_score, log_loss, mean_squared_error
from statsmodels.api import OLS
from pyfinance.ols import PandasRollingOLS
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from matplotlib import pyplot as plt
from statsmodels.tsa.api import Holt


META_PATHS = [
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_AVA_TERMINAL_ID'), 'MQL4', 'Files'),
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_DARWIN_TERMINAL_ID'), 'MQL4', 'Files'),
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_XTB_TERMINAL_ID'), 'MQL4', 'Files'),
]
STORAGE_PATH = abspath(chdir('G:\\storage'))
DATA_SOURCE = 'eod'
PER_SAHRE_COM = 0.0035
SEC_FEE = 23.1 # Per $1M
FINRA_FEE = 0.000119 # Per share

def peewee_to_df(table):
    fields = [f for f in dir(table) if isinstance(getattr(table, f), Field)]
    data = list(table.select(*[getattr(table, fld) for fld in fields]).tuples())
    df = DataFrame.from_records(data, columns=table._meta.fields)

    if 'id' in fields:
        df.set_index('id', inplace=True)
    return df

def periodize_returns(r, p=252):
    return r * sqrt(p)

def filenames(folder, resampled=False, mt=False):
    try:
        if mt:
            fs = [f for f in listdir(folder) if isfile(join(folder, f)) if 'DATA_MODEL' in f]
        else:
            path = join(STORAGE_PATH, folder)
            fs = [f for f in listdir(path) if isfile(join(path, f)) & ('.gitkeep' not in f)]
            if not resampled:
                fs = [i for i in fs if '_' not in i]
            else:
                fs = [i for i in fs if '_' in i]
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

def logloss(predicted, y, name):
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

def common(lst):
    return set.intersection(*map(set, [i for i in lst]))

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

def detrender(df, i=1):
    return (df - df.shift(i)) / ((df + df.shift(i)) / 2.0)

def exponential_smoothing(df, alpha):
    return df.ewm(alpha=alpha).mean()

def holt(df, chunk=100, smoothing=0.03, slope=0.1):
    cnt = int(len(df.index)/chunk)
    for i in range(cnt):
        if i == cnt:
            print('final')
        else:
            train = df.iloc[i*chunk:(i+1)*chunk]
            test = df.iloc[(i+1)*chunk:(i+2)*chunk]
            fit = Holt(asarray(train)).fit(smoothing_level=smoothing, smoothing_slope=slope)
            forecast = fit.forecast(len(test))
            try:
                rms = sqrt(mean_squared_error(test, forecast))
                print('RMS %s' % rms)
            except:
                pass
            plt.plot(train, color='b')
            plt.plot(test.index, forecast, lw=3, color='r')
    plt.show()
