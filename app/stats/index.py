from numpy import (cov, std, array, matrix, abs, mean, empty, sort, empty, sum, sqrt, log, exp,
    power, maximum, round, where, percentile, busday_count)
import scipy.stats as sc
from pandas import to_datetime, DataFrame, Series
from ffn import calc_stats

from app.utils import periodize_returns, comm, quantity, PER_SAHRE_COM, FINRA_FEE, SEC_FEE, CONSTANT_CAPITAL
from app.db import Strategy, Stats


def max_dd(drawdowns):
    return abs(drawdowns.min())

def beta(returns, benchmark):
    '''
    Measure of the risk arising from exposure to general market, a.k.a. systemic risk.
    '''
    covariance = cov(returns, benchmark)
    beta = covariance[0, 1] / covariance[1, 1]
    return beta

def vol(returns):
    return std(returns)

def treynor(returns, benchmark, rf):
    '''
    Relates excess return over the risk-free rate to the additional (systemic) risk taken.
    '''
    return (returns.mean() * sqrt(252) - rf) / beta(returns, benchmark)
  
def sharpe_ratio(returns, rf):
    '''
    Reward-to-variability ratio is a way to examine the performance by adjusting for its risk (variability in this case).
    '''
    if vol(returns) != 0:
        return (returns.mean() * sqrt(252) - rf) / vol(returns)
    else:
        return 0

def ir(returns, benchmark):
    '''
    The information ratio is often used to gauge the skill of managers of mutual funds, hedge funds, etc.
    In this case, it measures the active return of the manager's portfolio divided by the amount of risk,
    measured by variability, that the manager takes relative to the benchmark.
    '''
    diff = returns - benchmark
    return mean(diff) / vol(diff)

def modigliani(returns, benchmark, rf):
    '''
    It measures the returns of the portfolio, adjusted for the risk of the portfolio relative to that of benchmark.
    '''
    np_rf = empty(len(returns))
    np_rf.fill(rf)
    rdiff = returns - np_rf
    bdiff = benchmark - np_rf
    return (returns.mean() * sqrt(252) - rf) * (vol(rdiff) / vol(bdiff)) + rf

def var(returns, alpha):
    '''
    Value at risk, probability of occurrence for the defined loss.
    '''
    sorted_returns = sort(returns)
    index = int(alpha * len(sorted_returns))
    return abs(sorted_returns[index])

def cvar(returns, alpha):
    '''
    Conditional VaR, also known as mean excess loss, mean shortfall, tail value at risk,
    average value at risk or expected shortfall.
    '''
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
    diff = diff.clip()
    return sum(diff ** order) / len(returns)
 
def hpm(returns, threshold, order):
    threshold_array = empty(len(returns))
    threshold_array.fill(threshold)
    diff = returns - threshold_array
    diff = diff.clip()
    return sum(diff ** order) / len(returns)

def excess_var(returns, rf, alpha):
    return (returns.mean() * sqrt(252) - rf) / var(returns, alpha)

def conditional_sharpe(returns, rf, alpha):
    '''
    The ratio of expected excess return to the expected shortfall.
    '''
    return (returns.mean() * sqrt(252) - rf) / cvar(returns, alpha)

def omega_ratio(returns, rf, target=0):
    '''
    Probability weighted ratio of gains versus losses for threshold return target.
    '''
    return (returns.mean() * sqrt(252) - rf) / lpm(returns, target, 1)

def sortino(returns, rf, target=0):
    '''
    It is a modification of the Sharpe ratio that penalizes only those returns falling
    below a target and required rate of return.
    '''
    return (returns.mean() * sqrt(252) - rf) / sqrt(lpm(returns, target, 2))

def kappa_three(returns, rf, target=0):
    return (returns.mean() * sqrt(252)- rf) / power(lpm(returns=returns, threshold=target, order=3), 1/3.0)

def gain_loss(returns, target=0):
    return hpm(returns, target, 1) / lpm(returns, target, 1)

def upside_potential(returns, target=0):
    '''
    A measure of a return relative to the minimal acceptable return.
    '''
    return hpm(returns, target, 1) / sqrt(lpm(returns, target, 2))

def calmar(returns, rf):
    '''
    The Calmar ratio changes gradually and serves to smooth out the overachievement and
    underachievement periods of performance more readily than either the Sterling or
    Sharpe ratios.
    '''
    return (returns.mean() * sqrt(252) - rf) / max_dd(returns)

def drawdowns(cumulative):
    maxims = maximum.accumulate(cumulative.dropna())
    return cumulative - maxims

def average_dd(cumulative):
    return mean(drawdowns(cumulative))

def average_dd_squared(cumulative):
    return power(average_dd(cumulative), 2.0)

def sterling_ration(returns, rf):
    '''
    Measures return over average drawdown.
    '''
    add = average_dd(returns.cumsum())
    if add > 0:
        return (returns.mean() * sqrt(252)- rf) / add
    else:
        return None

def burke_ratio(returns, cumulative, rf):
    '''
    Similar to the Sterling ratio, the Burke ratio discounts the expected excess return
    by the square root of the average of the worst expected maximum drawdowns squared.
    '''
    return (returns.mean() * sqrt(252) - rf) / sqrt(average_dd_squared(cumulative))

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

def port_commissions(df, symbol):
    com = PER_SAHRE_COM + FINRA_FEE
    df['quantities'] = quantity(capital=CONSTANT_CAPITAL, price=df['{}_Close'.format(symbol)], alloc=1.0)
    df['c'] = comm(q=df['quantities'], p=com) + SEC_FEE / (1000000 / CONSTANT_CAPITAL)
    return df['c'], df['c'] / CONSTANT_CAPITAL, df['quantities']

def commissions(df, symbol, com=None):
    d = df.copy()
    if com is None:
        com = PER_SAHRE_COM + FINRA_FEE
    d['quantities'] = quantity(capital=CONSTANT_CAPITAL, price=df['{}_Close'.format(symbol)], alloc=1.0)
    d['c'] = comm(q=d['quantities'], p=com) + SEC_FEE / (1000000 / CONSTANT_CAPITAL)

    d['com'] = where((df['sig'] == 0) & (d['sig'].shift() == 1), d['c'], 0)
    d['com'] += where((df['sig'] == 1) & (d['sig'].shift() == 0), d['c'], 0)
    d['com'] += where((df['sig'] == 0) & (d['sig'].shift() == -1), d['c'], 0)
    d['com'] += where((df['sig'] == -1) & (d['sig'].shift() == 0), d['c'], 0)
    d['com'] += where((df['sig'] == 1) & (d['sig'].shift() == -1), d['c'], 0)
    d['com'] += where((df['sig'] == -1) & (d['sig'].shift() == 1), d['c'], 0)
    return d['com'], (d['com'] / CONSTANT_CAPITAL), d['quantities']

def percentiles(returns):
    p_list = [p for p in range(100)]
    res = []
    for per in p_list:
        res.append(percentile(returns, per))
    return array(res)

def alpha(returns, rf, market_return):
    '''
    This is based on the concept that riskier assets should have higher expected returns
    than less risky assets. If an asset's return is higher than the risk adjusted return,
    that asset is said to have 'positive alpha' or 'abnormal returns'.
    '''
    b = beta(returns=returns, benchmark=market_return)
    return returns.mean() - rf - b * (market_return.mean() * rf)

def average_trade(returns):
    return mean(returns)

def average_win(returns):
    return mean(where(returns > 0, returns, 0))

def average_loss(returns):
    return mean(where(returns <= 0, returns, 0))

def total_wins(returns):
    return sum(where(returns > 0, 1, 0))

def total_losses(returns):
    return sum(where(returns < 0, 1, 0))

def win_rate(returns):
    tw = total_wins(returns)
    return tw / (tw + total_losses(returns=returns))

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
    '''
    Ulcer Index measures downside risk, in terms of both depth and duration of price declines.
    '''
    m = maximum.accumulate(cumulative)
    r = (cumulative - m) / m * 100
    r2 = power(r, 2)
    return sum(r2) / len(cumulative)

def ulcer_performance_index(cumulative, r, rf):
    '''
    Ulcer Performance Index, a.k.a. Martin ratio is a Sharpe ratio with Ulcer Index instead of variability.
    '''
    return (periodize_returns(r=r) - rf) / ulcer_index(cumulative)

def drawdown_probability(cumulative):
    dd = drawdowns(cumulative=cumulative)
    dd = dd.loc[dd != 0]
    return abs(mean(percentiles(returns=dd)))

def return_probability(returns):
    returns = returns.loc[returns != 0]
    return abs(mean(percentiles(returns=returns)))

def average_mae(high, low, close, pos=0):
    return mae(high, low, close, pos).mean()

def average_mfe(high, low, close, pos=0):
    return mfe(high, low, close, pos).mean()

def correlation(returns):
    return returns.corr(returns.shift())

def returns_by_month():
    pass

def month_histogram(perf):
    perf.plot_histogram()
    plt.savefig()

def returns_by_year():
    pass

def rolling_sharpe():
    pass

def capital_utilization():
    pass

def average_trades_month(signals, retruns):
    return trade_count(signals=signals) / len(returns) * 30.416

def max_dd_duration(cumulative):
    i = (maximum.accumulate(cumulative) - cumulative).idxmax()
    j = cumulative[:i].idxmax()
    s = to_datetime(j).strftime ('%Y-%m-%d')
    e = to_datetime(i).strftime ('%Y-%m-%d')
    return busday_count(s, e)

def skew(returns):
    return 3.0 * (returns.mean() - (returns.max() + returns.min()) / 2.0) / returns.std()

def parkinson_vol(returns, per):
    ''' Parkinsons' volatility. '''
    var = (returns - returns.rolling(window=per, min_periods=per).mean())
    var2 = var * var
    return sqrt(var2.rolling(window=(per-1), min_periods=(per-1)).sum() * 1/(4*log(2)) * 252/(per-1))

def shanon_entropy(c):
    norm = c / float(sum(c))
    norm = norm[nonzero(norm)]
    H = -sum(norm * log2(norm))  
    return H

def mutual_info(x, y, bins):
    c_xy = histogram2d(x, y, bins)[0]
    return mutual_info_score(None, None, contingency=c_xy)

def incremental_diversification(returns, other):
    corr =  returns.corr(other)
    return -2 / log(1.0 - corr * corr)

def information_adjusted_corr(returns, other):
    corr =  returns.corr(other)
    p = -2 / incremental_diversification(returns=returns, other=other)
    acorr = sqrt(1.0 - power(2.0, p)) * corr
    assert acorr >= corr, 'We have error here'
    return acorr

def rolling_id(returns, other, per):
    corr =  returns.rolling(window=per, min_periods=per).corr(other)
    return -2 / log(1.0 - corr * corr)

def rolling_id_corr(returns, other, per):
    corr =  returns.rolling(window=per, min_periods=per).corr(other)
    p = -2 / rolling_id(returns=returns, other=other, per=per)
    return sqrt(1.0 - power(2.0, p)) * corr

def information_adjusted_beta(returns, other):
    return information_adjusted_corr(returns=returns, other=other) * sqrt(returns.var() / other.var())

def rolling_id_beta(returns, other, per):
    return rolling_id_corr(returns=returns, other=other, per=per) * \
        sqrt(returns.rolling(window=per, min_periods=per).var() / other.rolling(window=per, min_periods=per).var())

def profit_factor(returns):
    return (average_win(returns=returns) * total_wins(returns=returns)) / (average_loss(returns=returns) * total_losses(returns=returns))

def market_cap(pe, net_income):
    return pe * net_income

def revenue_per_employee(revenue, employees):
    return revenue / employees

def eps(net_income, shares_outstanding):
    return net_income / shares_outstanding

def working_capital_ratio(assets, liabilities):
    return assets / liabilities

def assets(cash, receivables, short_term_investments):
    return cash + receivables + short_term_investments

def acid_test(assets, inventory, liabilities):
    ''' Shows how well liabilities are covered by cash. '''
    return (assets - inventory) / liabilities

def debt_equity_ratio(debt, book_value):
    return debt / book_value

def roe(net_income, book_value):
    return net_income / book_value

def cagr(log_returns):
    return exp(log(1 + returns)/len(returns)) - 1

def common_sense(returns):
    profits = sum(where(returns > 0, returns, 0))
    losses = sum(where(returns < 0, returns, 0))
    return (percentile(returns, 95) * profits) / (percentile(returns, 5) * losses)

def stats_printout(returns, market):
    c = returns.cumsum()
    perf = calc_stats(returns)
    stats = perf.stats

    print('Basics -----------------------')
    start = stats['start']
    print('Start: %s' % start)
    end = stats['end']
    print('End: %s' % end)
    total_return = stats['total_return']
    print('Tital return: %.2f' % total_return)
    cagr = stats['cagr']
    print('CAGR: %.2f' % cagr)
    mtd = stats['mtd']
    print('Month to date: %.2f' % mtd)
    three_month = stats['three_month']
    print('3 months: %.2f' % three_month)
    six_month = stats['six_month']
    print('6 months: %.2f' % six_month)
    ytd = stats['ytd']
    print('YTD: %.2f' % ytd)
    three_year = stats['three_year']
    print('3 years: %.2f' % three_year)
    daily_skew = stats['daily_skew']
    print('Daily skew: %.2f' % daily_skew)
    daily_kurt = stats['daily_kurt']
    print('Daily kurtosis: %.2f' % daily_kurt)
    best_day = stats['best_day']
    print('Best day: %.2f' % best_day)
    worst_day = stats['worst_day']
    print('Worst day: %.2f' % worst_day)
    monthly_vol = stats['monthly_vol']
    print('Monthly volatility: %.2f' % monthly_vol)
    monthly_skew = stats['monthly_skew']
    print('Monthly skew: %.2f' % monthly_skew)
    monthly_kurt = stats['monthly_kurt']
    print('Monthly kurtosis: %.2f' % monthly_kurt)
    best_month = stats['best_month']
    print('Best month: %.2f' % best_month)
    avg_down_month = stats['avg_down_month']
    print('Average down month %s' % avg_down_month)
    worst_month = stats['worst_month']
    print('Worst month: %.2f' % worst_month)
    worst_year = stats['worst_year']
    print('Worst year: %.2f' % worst_year)
    yearly_mean = stats['yearly_mean']
    print('Yearly average: %.2f' % yearly_mean)
    yearly_vol = stats['yearly_vol']
    print('Yearly volatility: %.2f' % yearly_vol)
    yearly_skew = stats['yearly_skew']
    print('Yearly skew: %.2f' % yearly_skew)
    yearly_kurt = stats['yearly_kurt']
    print('Yearly kurtosis: %.2f' % yearly_kurt)
    avg_up_month = stats['avg_up_month']
    print('Average up month: %.2f' % avg_up_month)
    win_year_perc = stats['win_year_perc']
    print('Win years: %.2f' % win_year_perc)
    twelve_month_win_perc = stats['twelve_month_win_perc']
    print('12-mo win: %.2f' % twelve_month_win_perc)
    vv = vol(returns=returns)
    print('Volatility %.3f%%' % (vv * 100.0))
    amr = average_month_return(returns=returns) * 100.0
    print('Average month return %.3f%%' % amr)
    # trade_count(signals)
    pf = profit_factor(returns=returns)
    print('Profit factor %.2f%%' % pt)
    at = average_trade(returns=returns) * 100.0
    print('Average trade %.2f%%' % at)
    aw = average_win(returns=returns) * 100.0
    print('Average win %.2f%%' % aw)
    al = average_loss(returns=returns) * 100.0
    print('Average loss %.2f%%' % al)
    w = total_wins(returns=returns)
    print('Wins %s' % w)
    l = total_losses(returns=returns)
    print('Losses %s' % l)
    wr = win_rate(returns=returns) * 100.0
    print('Win rate %.3f%%' % wr)
    acor = correlation(returns=returns)
    print('Autocorrelation %.3f' % acor)

    print()
    print('Ratios -----------------------')
    print('Sharpe* %.3f' % (sharpe_ratio(returns, rf=0.0)))
    monthly_sharpe = stats['monthly_sharpe']
    print('Monthly Sharpe: %.2f' % monthly_sharpe)
    yearly_sharpe = stats['yearly_sharpe']
    print('Yearly Sharpe: %.2f' % yearly_sharpe)
    cs = common_sense(returns=returns)
    print('Common Sense Ratio: %.2f' % cs)
    b = beta(returns=returns, benchmark=market)
    print('Beta %.3f' % b)
    a = alpha(returns=returns.mean(), rf=0.0, market_return=market.mean())
    print('Alpha %.3f' % a)
    tr = treynor(returns=returns, benchmark=market, rf=0.0)
    print('Treynor* %.3f' % tr)
    infr = ir(returns=returns, benchmark=market)
    print('Information ratio %.3f' % infr)
    mod = modigliani(returns=returns, benchmark=market, rf=0.0)
    print('Modigliani ratio* %.3f' % mod)
    ora = omega_ratio(returns=returns, rf=0.0, target=0.0)
    print('Omega Ratio* %.3f' % ora)
    so = sortino(returns=returns, rf=0.0, target=0)
    print('Sortino Ratio* %.3f' % so)
    kt = kappa_three(returns=returns, rf=0.0, target=0.05)
    print('Kappa Three %.3f' % kt)
    up = upside_potential(returns=returns, target=0.0)
    print('Upside potential ratio %.3f' % up)
    cal = calmar(returns=returns, rf=0.0)
    print('Calmar Ratio* %.3f' % cal)
    ui = ulcer_index(cumulative=c)
    print('Ulcer Index %.3f' % ui)
    upi = ulcer_performance_index(cumulative=c, r=returns.mean(), rf=0.0)
    print('Ulcer Performance Index* %.3f' % upi)
    stra = sterling_ration(returns=returns, rf=0.0)
    if stra is not None:
        print('Sterling Ratio* %.3f' % stra)
    br = burke_ratio(returns=returns, cumulative=c, rf=0.0)
    print('Burke Ratio* %.3f' % br)

    print()
    print('VaR --------------------------')
    v = var(returns=returns, alpha=a)
    print('VaR %.3f' % v)
    cvv = cvar(returns=returns, alpha=a)
    print('Conditional VaR %.3f' % cvv)
    ev = excess_var(returns=returns, rf=0.0, alpha=a)
    print('Excess VaR* %.3f' % ev)
    cs = conditional_sharpe(returns=returns, rf=0.0, alpha=a)
    print('Conditional Sharpe* %.3f' % (cs * sqrt(252)))

    print()
    print('DD ---------------------------')
    dd = drawdowns(cumulative=c)
    mdd = max_dd(drawdowns=dd) * 100.0
    print('Max DD %.3f%%' % mdd)
    add = average_dd(cumulative=c) * 100.0
    print('Average DD %.2f%%' % add)
    adds = average_dd_squared(cumulative=c) * 100.0
    print('Average DD Squared %.3f%%' % adds)
    mdddur = max_dd_duration(cumulative=c)
    print('Max DD duration %s' % mdddur)
    dp = drawdown_probability(cumulative=c)
    print('Drawdown probability %.3f' % dp)
    rp = return_probability(returns=returns)
    print('Return probability %.3f' % rp)
    avg_drawdown_days = stats['avg_drawdown_days']
    print('Average DD duration %s' % avg_drawdown_days)
    #mae(high, low, close, pos=0)
    #mfe(high, low, close, pos=0)
    #max_mae(cumulative, mae)
    #min_mfe(cumulative, mfe)
    #average_mae(high, low, close, pos=0)
    #average_mfe(high, low, close, pos=0)

    print('* Values are annualized.')

def stats_values(returns, market):
    c = returns.cumsum()
    #perf = calc_stats(returns)
    #stats = perf.stats

    vv = vol(returns=returns) * 100.0
    amr = average_month_return(returns=returns) * 100.0
    # trade_count(signals)
    at = average_trade(returns=returns) * 100.0
    aw = average_win(returns=returns) * 100.0
    al = average_loss(returns=returns) * 100.0
    w = total_wins(returns=returns)
    l = total_losses(returns=returns)
    pf = profit_factor(returns=returns)
    wr = win_rate(returns=returns) * 100.0
    acor = correlation(returns=returns)
    sr = sharpe_ratio(returns, rf=0.0) * sqrt(252)
    b = beta(returns=returns, benchmark=market)
    a = alpha(returns=returns.mean(), rf=0.0, market_return=market.mean())
    tr = treynor(returns=returns, benchmark=market, rf=0.0)
    infr = ir(returns=returns, benchmark=market)
    mod = modigliani(returns=returns, benchmark=market, rf=0.0)
    ora = omega_ratio(returns=returns, rf=0.0, target=0.0)
    so = sortino(returns=returns, rf=0.0, target=0)
    kt = kappa_three(returns=returns, rf=0.0, target=0.05)
    up = upside_potential(returns=returns, target=0.0)
    cal = calmar(returns=returns, rf=0.0)
    ui = ulcer_index(cumulative=c)
    upi = ulcer_performance_index(cumulative=c, r=returns.mean(), rf=0.0)
    stra = sterling_ration(returns=returns, rf=0.0)
    br = burke_ratio(returns=returns, cumulative=c, rf=0.0)
    v = var(returns=returns, alpha=a)
    cvv = cvar(returns=returns, alpha=a)
    ev = excess_var(returns=returns, rf=0.0, alpha=a)
    cs = conditional_sharpe(returns=returns, rf=0.0, alpha=a)
    dd = drawdowns(cumulative=c)
    mdd = max_dd(drawdowns=dd) * 100.0
    add = average_dd(cumulative=c) * 100.0
    adds = average_dd_squared(cumulative=c) * 100.0
    mdddur = max_dd_duration(cumulative=c)
    dp = drawdown_probability(cumulative=c)
    rp = return_probability(returns=returns)
    cs = common_sense(returns=returns)
    #mae(high, low, close, pos=0)
    #mfe(high, low, close, pos=0)
    #max_mae(cumulative, mae)
    #min_mfe(cumulative, mfe)
    #average_mae(high, low, close, pos=0)
    #average_mfe(high, low, close, pos=0)
    '''
    start = stats['start']
    end = stats['end']
    total_return = stats['total_return']
    cagr = stats['cagr']
    mtd = stats['mtd']
    three_month = stats['three_month'],
    six_month = stats['six_month']
    ytd = stats['ytd']
    three_year = stats['three_year']
    daily_skew = stats['daily_skew']
    daily_kurt = stats['daily_kurt']
    best_day = stats['best_day']
    worst_day = stats['worst_day']
    monthly_sharpe = stats['monthly_sharpe']
    monthly_vol = stats['monthly_vol']
    monthly_skew = stats['monthly_skew']
    monthly_kurt = stats['monthly_kurt']
    best_month = stats['best_month']
    worst_month = stats['worst_month']
    yearly_sharpe = stats['yearly_sharpe']
    yearly_mean = stats['yearly_mean']
    yearly_vol = stats['yearly_vol']
    yearly_skew = stats['yearly_skew']
    yearly_kurt = stats['yearly_kurt']
    worst_year = stats['worst_year']
    avg_drawdown_days = stats['avg_drawdown_days']
    avg_up_month = stats['avg_up_month']
    avg_down_month = stats['avg_down_month']
    win_year_perc = stats['win_year_perc']
    twelve_month_win_perc = stats['twelve_month_win_perc']
    '''

    return {
        'volatility': vv,
        'average_month': amr,
        'average_trade': at,
        'average_win': aw,
        'average_loss': al,
        'total_wins': w,
        'total_losses': l,
        'win_rate': wr,
        'autocorrelation': acor,
        'sharpe': sr,
        'beta': b,
        'alpha': a,
        'treynor': tr,
        'information': infr,
        'win_rate': wr,
        'modigliani': mod,
        'omega': ora,
        'sortino': so,
        'kappa': kt,
        'upside': up,
        'calmar': cal,
        'ulcer_index': ui,
        'ulcer_performance_index': upi,
        'sterling': stra,
        'burke': br,
        'VaR': v,
        'cVaR': cvv,
        'eVaR': ev,
        'conditional_sharpe': cs,
        'max_dd': mdd,
        'average_dd': add,
        'average_dd_squared': adds,
        'max_dd_duration': mdddur,
        'dd_prob': up,
        'return_prob': rp,
        'profit_factor': pf,
        'common_sense': cs
        }
'''
'start': start,
        'end': end,
        'total_return': total_return,
        'cagr': cagr,
        'mtd': mtd,
        'three_month': three_month,
        'six_month': six_month,
        'ytd': ytd,
        'three_year': three_year,
        'daily_skew': daily_skew,
        'daily_kurt': daily_kurt,
        'best_day':best_day,
        'worst_day': worst_day,
        'monthly_sharpe': monthly_sharpe,
        'monthly_vol': monthly_vol,
        'monthly_skew': monthly_skew,
        'monthly_kurt': monthly_kurt,
        'best_month': best_month,
        'worst_month': worst_month,
        'yearly_sharpe':yearly_sharpe,
        'yearly_mean': yearly_mean,
        'yearly_vol': yearly_vol,
        'yearly_skew': yearly_skew,
        'yearly_kurt': yearly_kurt,
        'worst_year': worst_year,
        'avg_drawdown_days': avg_drawdown_days,
        'avg_up_month': avg_up_month,
        'avg_down_month': avg_down_month,
        'win_year_perc': win_year_perc,
        'twelve_month_win_perc': twelve_month_win_perc
'''