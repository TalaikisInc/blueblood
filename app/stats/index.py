from numpy import cov, std, array, matrix, abs, mean, empty, sort, empty, sum, sqrt, power, maximum, round, where, percentile
import scipy.stats as sc

from utils import periodize_returns
from db import Strategy, Stats


def max_dd(drawdowns):
    return abs(drawdowns.min())

def beta(returns, benchmark):
    m = matrix([returns, benchmark])
    return cov(m)[0][1] / std(benchmark)

def vol(returns):
    return std(returns)

def treynor(returns, benchmark, rf):
    return (returns.mean() - rf) / beta(returns, benchmark)
  
def sharpe_ratio(returns, rf):
    return (returns.mean() - rf) / vol(returns)

def ir(returns, benchmark):
    diff = returns - benchmark
    return mean(diff) / vol(diff)

def modigliani(returns, benchmark, rf):
    np_rf = empty(len(returns))
    np_rf.fill(rf)
    rdiff = returns - np_rf
    bdiff = benchmark - np_rf
    return (returns.mean() - rf) * (vol(rdiff) / vol(bdiff)) + rf

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

def excess_var(returns, rf, alpha):
    return (returns.mean() - rf) / var(returns, alpha)

def conditional_sharpe(returns, rf, alpha):
    return (returns.mean() - rf) / cvar(returns, alpha)

def omega_ratio(returns, rf, target=0):
    return (returns.mean() - rf) / lpm(returns, target, 1)
 
def sortino(returns, rf, target=0):
    return (returns.mean() - rf) / sqrt(lpm(returns, target, 2))

def kappa_three(returns, rf, target=0):
    return (returns.mean() - rf) / power(lpm(returns, target, 3), float(1/3))
 
def gain_loss(returns, target=0):
    return hpm(returns, target, 1) / lpm(returns, target, 1)

def upside_potential(returns, target=0):
    return hpm(returns, target, 1) / sqrt(lpm(returns, target, 2))

def calmar(returns, rf):
    return (returns.mean() - rf) / max_dd(returns)

def drawdowns(cumulative):
    maxims = maximum.accumulate(cumulative.dropna())
    return cumulative - maxims

def average_dd(cumulative):
    return mean(drawdowns(cumulative))

def average_dd_squared(cumulative):
    return power(average_dd(cumulative), 2.0)

def sterling_ration(retruns, cumulative, rf):
    return (returns.mean() - rf) / average_dd(cumulative)

def burke_ratio(returns, cumulative, rf):
    return (returns.mean() - rf) / sqrt(average_dd_squared(cumulative))

def average_month_return(returns):
    return sum(returns) / len(returns) * 30.416

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
    return array(res)

def alpha(portfolio_return, rf, beta, market_return):
    return portfolio_return - rf - beta * (market_return * rf)

def average_trade(returns):
    return mean(returns)

def average_win(returns):
    return mean(where(returns > 0, returns, 0))

def average_loss(returns):
    return mean(where(returns <= 0, returns, 0))

def total_wins(returns):
    return sum(where(returns > 0, 1, 0))

def total_losses(returns):
    return sum(where(returns <= 0, 1, 0))

def win_rate(returns):
    w = total_wins(returns)
    l = sum(where(returns <= 0, 1, 0))
    if l > 0:
        return w / l
    else:
        return 0

def mae(high, low, close, pos=0):
    if pos == 1:
        return cl(close, low)
    else:
        return hc(high, close)

def mfe(high, low, close, pos=0):
    if pos == 1:
        return hc(high, close)
    else:
        return cl(close, low)        

def max_mae(cumulative, mae):
    return (cumulative - mae).max()

def min_mfe(cumulative, mfe):
    return (mfe - cumulative).min()

def cl(close, low):
    return (close - low)

def hc(high, close):
    return (high - close)

def ulcer_index(cumulative):
    m = maximum.accumulate(cumulative)
    r = (cumulative - m) / m * 100
    r2 = power(r, 2)
    return sum(r2) / len(cumulative)

def ulcer_performance_index(cumulative, r, rf):
    return (periodize_returns(r=r) - rf) / ulcer_index(cumulative)

def drawdown_probability(cumulative):
    dd = drawdowns(cumulative=cumulative)
    dd = dd.loc[dd != 0]
    return mean(percentiles(returns=dd)) / 100

def return_probability(returns):
    returns = returns.loc[returns != 0]
    return mean(percentiles(returns=returns)) / 100

def average_mae(high, low, close, pos=0):
    return mae(high, low, close, pos).mean()

def average_mfe(high, low, close, pos=0):
    return mfe(high, low, close, pos).mean()

def best_month():
    pass

def worst_month():
    pass

def best_day():
    pass

def worst_day():
    pass

def best_year():
    pass

def worst_year():
    pass

def returns_by_month():
    pass

def returns_by_year():
    pass

def rolling_sharpe():
    pass

def capital_utilization():
    pass

def average_up_month(returns):
    pass

def average_down_month(returns):
    pass

def average_trades_month(signals, retruns):
    return trade_count(signals=signals) / len(returns) * 30.416

def average_dd_duration():
    pass

def run_stats():
    for strategy in Strategy.select():
        returns = DataFrame() # READ RETURNS HERE
        data = DataFrame()
        pos = 0 # get position type from strategy
        cumulative = returns.cumsum()
        benchmark = DataFrame()
        signals = DataFrame()
        ma = mae(high=data['High'], low=data['Low'], close=data['Close'], pos=pos)
        mf = mae(high=data['High'], low=data['Low'], close=data['Close'], pos=pos)
        rf = 0.05
        alpha = 0.05
        target = 0.05
        b = beta(returns=returns, benchmark=benchmark)
        Stats.create(
            strategy=strategy,
            max_dd=max_dd(drawdowns=drawdowns(cumulative=cumulative)),
            beta=b,
            vol=vol(returns=returns),
            treynor=treynor(returns=returns, benchmark=benchmark, rf=rf),
            sharpe_ratio=sharpe_ratio(returnsreturns, rf=rf),
            ir=ir(returns=returns, benchmark=benchmark),
            modigliani=modigliani(returns=returns, benchmark=benchmark, rf=rf),
            var=var(returns=returns, alpha=alpha),
            cvar=cvar(returns=returns, alpha=alpha),
            excess_var=excess_var(returns=returns, rf=rf, alpha=alpha),
            conditional_sharpe=conditional_sharpe(returns=returns, rf=rf, alpha=alpha),
            omega_ratio=omega_ratio(returns=returns, rf=rf, target=target),
            sortino=sortino(returns=returns, rf, target=target),
            kappa_three=kappa_three(returns=returns, rf=rf, target=target),
            gain_loss=gain_loss(returns=returns, target=target),
            upside_potential=upside_potential(returns=returns, target=target),
            calmar=calmar(returns=returns, rf=rf),
            average_dd=average_dd(cumulative=cumulative=cumulative),
            average_dd_squared=average_dd_squared(cumulative=cumulative),
            sterling_ration=sterling_ration(retruns=retruns, cumulative=cumulative, rf=rf),
            burke_ratio=burke_ratio(returns=returns, cumulative=cumulative, rf=rf),
            average_month_return=average_month_return(returns=returns),
            average_trades_month=average_trades_month(signals=signals, retruns=retruns),
            average_dd_duration=
            trade_count=trade_count(signals=signals),
            alpha=alpha(portfolio_return=returns, rf=rf, beta=b, market_return=benchmark),
            average_trade=average_trade(returns=returns),
            average_win=average_win(returns=returns),
            average_loss=average_loss(returns=returns),
            total_wins=total_wins(returns=returns),
            total_losses=total_losses(returns=returns),
            win_rate=win_rate(returns=returns),
            # thos two should show only on trade days:
            average_mae=average_mae(high=data['High'], lowdata['Low'], closedata['Close'], pos=pos)
            average_mfe=average_mfe(high=data['High'], low=data['Low'], close=data['Close'], pos=pos)
            max_mae=max_mae(cumulative=cumulative, mae=ma),
            min_mfe=min_mfe(cumulative=cumulative, mfe=mf),
            ulcer_index=ulcer_index(cumulative=cumulative),
            ulcer_performance_index=ulcer_performance_index(cumulative=cumulative, r=returns.mean(), rf=rf),
            best_month=
            worst_month=
            best_day=
            worst_day=
            best_year=
            worst_year=
            average_up_month=
            average_down_month=
            capital_utilization=
            rolling_sharpe=
            returns_by_month=
            returns_by_year=
            percentiles=
            drawdown_probability=
            return_probability=
        )
