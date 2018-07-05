from numpy import cov, std, matrix, abs, mean, empty, sort, empty, sum, sqrt, pow, maximum, round, where, percentile
import scipy.stats as sc


def max_dd(drawdowns):
    return abs(drawdowns.min())

def beta(returns, benchmark):
    m = matrix([returns, benchmark])
    return cov(m)[0][1] / std(benchmark)

def vol(returns):
    return std(returns)

def treynor(er, returns, benchmark, rf):
    return (er - rf) / beta(returns, benchmark)
  
def sharpe_ratio(er, returns, rf):
    return (er - rf) / vol(returns)

def ir(returns, benchmark):
    diff = returns - benchmark
    return mean(diff) / vol(diff)

def modigliani(er, returns, benchmark, rf):
    np_rf = empty(len(returns))
    np_rf.fill(rf)
    rdiff = returns - np_rf
    bdiff = benchmark - np_rf
    return (er - rf) * (vol(rdiff) / vol(bdiff)) + rf

def value_at_risk(data, confidence_level):
    returns_mean = data.mean()
    returns_volatility = data.std()
    params = sc.t.fit(data)
    alpha = sc.t.ppf(q=(1-confidence_level), df=params[0], loc=returns_mean, scale=returns_volatility)
    return 1 - (alpha + 1)

def var(returns, alpha):
    sorted_returns = sort(returns)
    index = int(alpha * len(sorted_returns))
    return abs(sorted_returns[index])

 def cvar(returns, alpha):
    sorted_returns = sort(returns)
    index = int(alpha * len(sorted_returns))
    sum_var = sorted_returns[0]
    for i in range(1, index):
        sum_var += sorted_returns[i]
    return abs(sum_var / index)

def lpm(returns, threshold, order):
    threshold_array = empty(len(returns))
    threshold_array.fill(threshold)
    diff = threshold_array - returns
    diff = diff.clip(min=0)
    return sum(diff ** order) / len(returns)
 
def hpm(returns, threshold, order):
    threshold_array = empty(len(returns))
    threshold_array.fill(threshold)
    diff = returns - threshold_array
    diff = diff.clip(min=0)
    return sum(diff ** order) / len(returns)

def excess_var(er, returns, rf, alpha):
    return (er - rf) / var(returns, alpha)

def conditional_sharpe(er, returns, rf, alpha):
    return (er - rf) / cvar(returns, alpha)

def omega_ratio(er, returns, rf, target=0):
    return (er - rf) / lpm(returns, target, 1)
 
def sortino(er, returns, rf, target=0):
    return (er - rf) / sqrt(lpm(returns, target, 2))

def kappa_three(er, returns, rf, target=0):
    return (er - rf) / pow(lpm(returns, target, 3), float(1/3))
 
def gain_loss(returns, target=0):
    return hpm(returns, target, 1) / lpm(returns, target, 1)

def upside_potential(returns, target=0):
    return hpm(returns, target, 1) / sqrt(lpm(returns, target, 2))

def calmar(er, returns, rf):
    return (er - rf) / max_dd(returns)

def drawdowns(cumulative):
    maxims = maximum.accumulate(cumulatives.dropna())
    return cumulative - maxims

def average_dd(cumulative):
    return mean(drawdowns(cumulative))

def average_dd_squared(cumulative):
    return pow(average_dd(cumulative), 2.0)

def sterling_ration(er, returns, rf, periods):
    return (er - rf) / average_dd(returns, periods)

def burke_ratio(er, returns, rf, periods):
    return (er - rf) / sqrt(average_dd_squared(returns, periods))

def average_month_return(returns):
    return sum(returns) / len(returns) * 30.416

def best_month():
    pass

def worst_month():
    pass

def returns_by_month():
    pass

def returns_by_year():
    pass

def trade_count(signals):
    trades = where((signals == 0) & (signals.shift() == 1), 1, 0)
    trades += where((signals == 1) & (signals.shift() == 0), 1, 0)
    trades += where((signals == 0) & (signals.shift() == -1), 1, 0)
    trades += where((signals == -1) & (signals.shift() == 0), 1, 0)
    trades += where((signals == 1) & (signals.shift() == -1), 1, 0)
    trades += where((signals == -1) & (signals.shift() == 1), 1, 0)
    return trades.sum()


def commissions(signals, com):
    com = where((signals == 0) & (signals.shift() == 1), com, 0)
    com += where((signals == 1) & (signals.shift() == 0), com, 0)
    com += where((signals == 0) & (signals.shift() == -1), com, 0)
    com += where((signals == -1) & (signals.shift() == 0), com, 0)
    com += where((signals == 1) & (signals.shift() == -1), com, 0)
    com += where((signals == -1) & (signals.shift() == 1), com, 0)
    return com

def percentiles(returns):
    p_list = [p for p in range(100)]
    res = []
    for per in p_list:
        res.append(percentile(returns, per))
    return res
