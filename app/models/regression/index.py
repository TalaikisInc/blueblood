from numpy import array, diff, vstack, linalg, ones

from pyfinance import ols


def regression(x, y):
    x = array(x)
    y = array(y)
    A = vstack([x, ones(len(x))]).T
    result = linalg.lstsq(A, y, rcond=None)[0]
    beta = result[0]
    alpha = result[1]

    return(alpha, beta)

def rolling(y, data, per):
    ''' returns alpha,  beta amd p values.'''
    rolling = ols.PandasRollingOLS(y=y, x=data, window=per)
    return rolling
