from numpy import log, cumsum, log2, nonzero, sum, histogram2d, sqrt, polyfit, subtract, std, nan, inf
from numpy.polynomial import Polynomial
from pandas import DataFrame, Series, cut
from peewee import Field
from sklearn.metrics import mutual_info_score, log_loss, mean_squared_error
from statsmodels.api import OLS
from pyfinance.ols import PandasRollingOLS
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from matplotlib import pyplot as plt
from statsmodels.tsa.api import Holt

from .vars import STORAGE_PATH
from app.data import save_one
from app.variables import USED_DATA
from .date_utils import ensure_latest


def peewee_to_df(table):
    fields = [f for f in dir(table) if isinstance(getattr(table, f), Field)]
    data = list(table.select(*[getattr(table, fld) for fld in fields]).tuples())
    df = DataFrame.from_records(data, columns=table._meta.fields)

    if 'id' in fields:
        df.set_index('id', inplace=True)
    return df

def periodize_returns(r, p=252):
    return r * sqrt(p)

def log_returns(x):
    return log(x)

def get_dividends_splits(close, adjusted):
    '''Outputs should be classified into: dividend, split or white noise.'''
    return adjusted - close

def vwap(v, h, l):
    return cumsum(v * (h + l) / 2) / cumsum(v)

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

def dedup(df):
    return df[~df.index.duplicated(keep='first')].replace([inf, -inf], nan).dropna(how='all')

def future_price(S, t, r=0.05):
    '''
    S = Current market price of the underlying stock/index
    R = Risk free rate of return
    T = Time in days
    '''
    return S * exp(r*t)

def intersection(lists):
    out = lists[0]
    for i in range(1, len(lists)):
        out = list(set(lists[i]).intersection(out))

    return out

def collect_used_data():
    for s in USED_DATA:
        print('Getting %s ' %s)
        save_one(s)

class NamedDict(dict):
    def __init__(self, *args, **kwargs):
        try:
            self._name = kwargs.pop('name')
        except KeyError:
            raise KeyError('A \'name\' keyword argument should be supplied!')
        super(NamedDict, self).__init__(*args, **kwargs)

    @classmethod
    def fromkeys(cls, name, seq, value=None):
        return cls(dict.fromkeys(seq, value), name=name)

    @property
    def name(self):
        return self._name

def reinvested(df, symbol):
    start_vals = cut(df['sig'], bins=(0,1), labels=[1])

