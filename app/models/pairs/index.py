import statsmodels.tsa.stattools as ts
from numpy import ones, log, subtract, sqrt, log, polyfit, std, inf, where
from statsmodels.api import add_constant, OLS

from app.models.kalman import kalman_average, kalman_regression
from app.utils import zscore


def root_test(residuals):
    cadf = ts.adfuller(residuals)

    return {
        'cadf': cadf[0],
        'p-value': cadf[1],
        'data_points': cadf[3],
        'critical_values': cadf[4]
    }

def half_life(spread):
    lag = spread.shift(1)
    lag.iloc[0] = lag.iloc[1]
    ret = spread - lag
    ret.iloc[0] = ret.iloc[1]
    lag2 = add_constant(lag)
    model = OLS(ret, lag2)
    res = model.fit()
    halflife = int(round(-log(2) / res.params[1], 0))

    if halflife <= 0:
        halflife = 1
    return halflife

def find_cointegrated_pairs(dataframe, critial_level=0.05):
    n = dataframe.shape[1]
    pvalue_matrix = ones((n, n))
    keys = dataframe.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            stock1 = dataframe[keys[i]]
            stock2 = dataframe[keys[j]]
            result = ts.coint(stock1, stock2)
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            if pvalue < critial_level:
                pairs.append((keys[i], keys[j], pvalue))
    return pvalue_matrix, pairs

def spread(df):
    state_means = kalman_regression(kalman_average(df.x), kalman_average(df.y))

    df['hr'] = - state_means[:,0]
    df['spread'] = df.y + (df.x * df.hr)

    halflife = half_life(df['spread'])
    print('Half life: %s' % halflife)

    df['zScore'] = zscore(data=df.spread, pe=halflife)

def hurst(ts):
    lags = range(2, 63)
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    lt = log(tau)
    lt = where(lt == inf, 0, lt)
    lt = where(lt == -inf, 0, lt)
    poly = polyfit(log(lags), lt, 1)
    return poly[0] * 2.0
