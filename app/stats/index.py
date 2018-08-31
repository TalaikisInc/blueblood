from datetime import datetime, timedelta

from numpy import (cov, std, array, matrix, abs, mean, empty, sort, empty, sum, sqrt, log, exp,
    power, maximum, minimum, round, where, percentile, busday_count, unique)
import scipy.stats as sc
from pandas import to_datetime, DataFrame, Series, concat
from matplotlib import pyplot as plt, cm
from seaborn import despine, heatmap

from app.data import get_pickle
from app.utils import periodize_returns, comm, quantity, PER_SAHRE_COM, FINRA_FEE, SEC_FEE, CONSTANT_CAPITAL, save_plot
from app.db import Strategy, Stats


def max_dd(returns):
    dd = drawdowns(cumulative=returns.cumsum())
    return abs(dd.min())

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
        return (mean(returns) - rf) / vol(returns) * sqrt(252)
    else:
        return 0

def monthly_sharpe(returns):
    rf = 0.0
    return (returns.resample('1M').sum().mean() - rf) / returns.resample('1M').sum().std() * sqrt(12)

def weekly_sharpe(returns):
    rf = 0.0
    return (returns.resample('1W').sum().mean() - rf) / returns.resample('1W').sum().std() * sqrt(52)

def yearly_sharpe(returns):
    rf = 0.0
    return (returns.resample('1Y').sum().mean() - rf) / returns.resample('1Y').sum().std()

def ir(returns, benchmark):
    '''
    The information ratio is often used to gauge the skill of managers of mutual funds, hedge funds, etc.
    In this case, it measures the active return of the manager's portfolio divided by the amount of risk,
    measured by variability, that the manager takes relative to the benchmark.
    '''
    diff = returns - benchmark
    v = vol(diff)
    if v > 0:
        return mean(diff) / v
    else:
        return 0

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
    return (mean(returns) * sqrt(252) - rf) / sqrt(lpm(returns=returns, threshold=target, order=2))

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
    return mean(returns) - rf - b * (mean(market_return) * rf)

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
    r = (cumulative - m) / m * 100.0
    r2 = power(r, 2)
    return sum(r2) / len(cumulative.index)

def ulcer_performance_index(cumulative, r, rf):
    '''
    Ulcer Performance Index, a.k.a. Martin ratio is a Sharpe ratio with Ulcer Index instead of variability.
    '''
    return (r - rf) / ulcer_index(cumulative) * sqrt(252)

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

def rolling_sharpe(returns, rf, per):
    return ((returns.rolling(window=per, min_periods=per).mean() - rf) / returns.rolling(window=per, min_periods=per).std()) * sqrt(252)

def average_trades_month(signals, retruns):
    return trade_count(signals=signals) / len(returns) * 30.416

def max_dd_duration(cumulative):
    i = (maximum.accumulate(cumulative) - cumulative).idxmax()
    j = cumulative[:i].idxmax()
    s = to_datetime(j).strftime ('%Y-%m-%d')
    e = to_datetime(i).strftime ('%Y-%m-%d')
    return busday_count(s, e)

def skew(returns):
    return 3.0 * (mean(returns) - (returns.max() + returns.min()) / 2.0) / vol(returns)

def rolling_skew(returns, per):
    return 3.0 * (returns.rolling(window=per, min_periods=per).mean() - \
        (returns.rolling(window=per, min_periods=per).max() + \
        returns.rolling(window=per, min_periods=per).min()) / 2.0) / \
        returns.rolling(window=per, min_periods=per).std()

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
    return (average_win(returns=returns) * total_wins(returns=returns)) / abs(average_loss(returns=returns) * total_losses(returns=returns))

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

def get_years_count(returns):
    return len(unique(returns.index.year))

def cagr(returns):
    starting_cap = 100000.0
    c = (1 + returns.cumsum()) * starting_cap
    a = c.tail(1).values[0] / c.head(1).values[0]
    years = 1.0 / get_years_count(returns=returns)
    return (power(a, years) - 1) * 100.0

def common_sense(returns):
    profits = sum(where(returns > 0, returns, 0))
    losses = sum(where(returns < 0, returns, 0))
    return (percentile(returns, 95) * profits) / (percentile(returns, 5) * losses)

def win_loss_ratio(returns):
    return average_win(returns=returns) / average_loss(returns=returns)

def cpc_index(returns):
    return profit_factor(returns=returns) * win_rate(returns=returns) * win_loss_ratio(returns=returns)

def tail_ratio(returns):
    return percentile(returns, 95) / percentile(returns, 5)

def outlier_win_ratio(returns):
    return percentile(returns, 99) / average_win(returns=returns)

def outlier_loss_ratio(returns):
    return percentile(returns, 1) / average_loss(returns=returns)

def get_start(returns):
    return returns.head(1).index.strftime('%Y-%m-%d').values[0]

def get_end(returns):
    return returns.tail(1).index.strftime('%Y-%m-%d').values[0]

def total_return(returns):
    return returns.cumsum().tail(1).values[0] * 100.0

def ytd(returns):
    this_y = datetime.now().year
    returns = returns.loc['{}-01-01'.format(this_y):]
    return returns.cumsum().tail(1).values[0] * 100.0

def mtd(returns):
    this_m = datetime.now().month
    this_y = datetime.now().year
    returns = returns.loc['{}-{}-01'.format(this_y, this_m):]
    return returns.cumsum().tail(1).values[0] * 100.0

def mos(returns, m):
    returns = returns.iloc[-(m*21):-1]
    return returns.cumsum().tail(1).values[0] * 100.0

def best_day(returns):
    return returns.max() * 100.00

def worst_day(returns):
    return returns.min() * 100.00

def best_month(returns):
    return returns.resample('1M').sum().max() * 100.00

def worst_month(returns):
    return returns.resample('1M').sum().min() * 100.00

def daily_skew(returns):
    return returns.skew()

def daily_kurtosis(returns):
    return returns.kurtosis()

def monthly_vol(returns):
    return returns.resample('1M').sum().std() * 100.0

def monthly_skew(returns):
    return returns.resample('1M').sum().skew()

def monthly_kurtosis(returns):
    return returns.resample('1M').sum().kurtosis()

def worst_year(returns):
    return returns.resample('1Y').sum().min() * 100.0

def returns_by_year(returns):
    return returns.resample('1Y').sum() * 100.0

def returns_by_month(returns):
    return returns.resample('1M').sum() * 100.0

def returns_by_week(returns):
    return returns.resample('1W').sum() * 100.0

def returns_by_day(returns):
    return returns * 100.0

def save_yearly_returns(returns):
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    despine()
    ax.yaxis.grid(linestyle=':')
    returns.plot(kind='bar')
    ax.set_title('Yearly Returns, %', fontweight='bold')
    ax.set_ylabel('%')
    ax.set_xlabel('Year')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.xaxis.grid(False)
    save_plot(plt=plt, folder='index', name='yearly_returns')

def cumulate_returns(x):
    return x.cumsum()[-1]

def monthly_heatmap(returns):
    returns = returns.groupby([lambda x: x.year, lambda x: x.month]).apply(cumulate_returns)
    returns = returns.to_frame().unstack()
    returns = round(returns, 3)
    returns.rename(columns={ 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
        inplace=True)
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    heatmap(returns, annot=True, fmt='0.12f', annot_kws={'size': 8}, alpha=1.0, center=0.0, cbar=False, cmap=cm.RdYlGn, ax=ax)
    ax.set_title('Monthly Returns, %', fontweight='bold')
    save_plot(plt=plt, folder='index', name='monthly_returns')

def plot_returns(returns):
    d = returns_by_day(returns=returns)
    y = returns_by_year(returns=returns)
    save_yearly_returns(returns=y)
    monthly_heatmap(returns=d)

def best_year(returns):
    return returns.resample('1Y').sum().max() * 100.0

def average_down_month(returns):
    m = returns.resample('1M').sum()
    return mean(where(m <= 0, m , 0)) * 100.0

def average_up_month(returns):
    m = returns.resample('1M').sum()
    return mean(where(m > 0, m , 0)) * 100.0

def yearly_skew(returns):
    return returns.resample('1Y').sum().skew()

def yearly_kurtosis(returns):
    return returns.resample('1Y').sum().kurtosis()

def yearly_vol(returns):
    return returns.resample('1Y').sum().std() * 100.0

def win_years_percent(returns):
    y = returns.resample('1Y').sum()
    return sum(where(y > 0, 1, 0)) / len(y.index)

def win_months_percent(returns):
    y = returns.resample('1M').sum()
    return sum(where(y > 0, 1, 0)) / len(y.index)

def win_weeks_percent(returns):
    y = returns.resample('1W').sum()
    return sum(where(y > 0, 1, 0)) / len(y.index)

def yearly_mean(returns):
    return returns.resample('1Y').sum().mean() * 100.0

def stats_printout(returns, tf=1440):
    if tf == 1440:
        market = get_pickle('tiingo', 'SPY')['SPY_AdjClose'].pct_change()
        df = concat([returns, market], axis=1)
        df.columns = ['returns', 'market']
        df = df.dropna()
        returns = df['returns']
        market = df['market']
    c = returns.cumsum()

    print('Basics -----------------------')
    start = get_start(returns=returns)
    print('Start: %s' % start)
    end = get_end(returns=returns)
    print('End: %s' % end)
    ys = get_years_count(returns=returns)
    print('years: %.0f' % ys)
    tret = total_return(returns=returns)
    print('Total return: %.2f%%' % tret)
    # @TODO initial valeus should be already reinvested
    cgr = cagr(returns=returns)
    print('CAGR: %.2f%%' % cgr)
    _ytd = ytd(returns=returns)
    print('YTD: %.2f%%' % _ytd)
    _mtd = mtd(returns=returns)
    print('Month to date: %.2f%%' % _mtd)
    three_month = mos(returns=returns, m=3)
    print('3 months: %.2f%%' % three_month)
    six_month = mos(returns=returns, m=6)
    print('6 months: %.2f%%' % six_month)
    three_year = mos(returns=returns, m=36)
    print('3 years: %.2f%%' % three_year)
    dailyskew = daily_skew(returns=returns)
    print('Daily skew: %.2f' % dailyskew)
    daily_kurt = daily_kurtosis(returns=returns)
    print('Daily kurtosis: %.2f' % daily_kurt)
    bestday = best_day(returns)
    print('Best day: %.2f%%' % bestday)
    worstday = worst_day(returns)
    print('Worst day: %.2f%%' % worstday)
    monthlyvol = monthly_vol(returns=returns)
    print('Monthly volatility: %.2f%%' % monthlyvol)
    monthlyskew = monthly_skew(returns=returns)
    print('Monthly skew: %.2f' % monthlyskew)
    monthlykurt = monthly_skew(returns=returns)
    print('Monthly kurtosis: %.2f' % monthlykurt)
    bestmonth = best_month(returns=returns)
    print('Best month: %.2f%%' % bestmonth)
    worstmonth = worst_month(returns=returns)
    print('Worst month: %.2f%%' % worstmonth)
    bestyear = best_year(returns=returns)
    print('Best year: %.2f%%' % bestyear)
    worstyear = worst_year(returns=returns)
    print('Worst year: %.2f%%' % worstyear)
    yearlymean = yearly_mean(returns=returns)
    print('Yearly average: %.2f%%' % yearlymean)
    yearlyvol = yearly_vol(returns=returns)
    print('Yearly volatility: %.2f%%' % yearlyvol)
    yearlyskew = yearly_skew(returns=returns)
    print('Yearly skew: %.2f' % yearlyskew)
    yearly_kurt = yearly_kurtosis(returns=returns)
    print('Yearly kurtosis: %.2f' % yearly_kurt)
    avg_down_month = average_down_month(returns=returns)
    print('Average down month %.2f%%' % avg_down_month)
    avg_up_month = average_up_month(returns=returns)
    print('Average up month: %.2f%%' % avg_up_month)
    win_year_perc = win_years_percent(returns=returns) * 100.0
    print('Win years: %.2f%%' % win_year_perc)
    win_mo_perc = win_months_percent(returns=returns) * 100.0
    print('Win months: %.2f%%' % win_mo_perc)
    win_w_perc = win_weeks_percent(returns=returns) * 100.0
    print('Win weeks: %.2f%%' % win_w_perc)
    vv = vol(returns=returns)
    print('Volatility %.3f%%' % (vv * 100.0))
    amr = average_month_return(returns=returns) * 100.0
    print('Average month return %.3f%%' % amr)
    pf = profit_factor(returns=returns)
    print('Profit factor %.2f' % pf)
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
    monthlysharpe = monthly_sharpe(returns=returns)
    print('Monthly Sharpe: %.2f' % monthlysharpe)
    weeklysharpe = weekly_sharpe(returns=returns)
    print('Weekly Sharpe: %.2f' % weeklysharpe)
    yearlysharpe = yearly_sharpe(returns=returns)
    print('yearly Sharpe: %.2f' % yearlysharpe)
    cs = common_sense(returns=returns)
    print('Common Sense Ratio: %.2f' % cs)
    if tf == 1440:
        b = beta(returns=returns, benchmark=market)
        print('Beta %.3f' % b)
        a = alpha(returns=returns, rf=0.0, market_return=market)
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
    wlr = win_loss_ratio(returns=returns)
    print('Win-Loss Ratio %.2f' % wlr)
    cpc = cpc_index(returns=returns)
    print('CPC Index %.3f' % cpc)
    tailr = tail_ratio(returns=returns)
    print('Tail ratio %.3f' % tailr)
    owr = outlier_win_ratio(returns=returns)
    print('Outlier win ratio %.3f' % owr)
    olr = outlier_loss_ratio(returns=returns)
    print('Outlier loss ratio %.3f' % olr)

    if tf == 1440:
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
    mdd = max_dd(returns=returns) * 100.0
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

    print('* Values are annualized.')

def stats_values(returns):
    market = get_pickle('tiingo', 'SPY')['SPY_AdjClose'].pct_change()
    df = concat([returns, market], axis=1)
    df.columns = ['returns', 'market']
    df = df.dropna()
    returns = df['returns']
    market = df['market']
    c = returns.cumsum()

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
    sr = sharpe_ratio(returns, rf=0.0)
    b = beta(returns=returns, benchmark=market)
    a = alpha(returns=returns, rf=0.0, market_return=market)
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
    mdd = max_dd(returns=returns) * 100.0
    add = average_dd(cumulative=c) * 100.0
    adds = average_dd_squared(cumulative=c) * 100.0
    mdddur = max_dd_duration(cumulative=c)
    dp = drawdown_probability(cumulative=c)
    rp = return_probability(returns=returns)
    cs = common_sense(returns=returns)
    wlr = win_loss_ratio(returns=returns)
    cpc = cpc_index(returns=returns)
    tailr = tail_ratio(returns=returns)
    owr = outlier_win_ratio(returns=returns)
    olr = outlier_loss_ratio(returns=returns)
    start = get_start(returns=returns)
    end = get_end(returns=returns)
    ys = get_years_count(returns=returns)
    tret = total_return(returns=returns)
    cgr = cagr(returns=returns)
    _ytd = ytd(returns=returns)
    _mtd = mtd(returns=returns)
    three_month = mos(returns=returns, m=3)
    six_month = mos(returns=returns, m=6)
    three_year = mos(returns=returns, m=36)
    dailyskew = daily_skew(returns=returns)
    daily_kurt = daily_kurtosis(returns=returns)
    bestday = best_day(returns)
    worstday = worst_day(returns)
    monthlyvol = monthly_vol(returns=returns)
    monthlyskew = monthly_skew(returns=returns)
    monthlykurt = monthly_skew(returns=returns)
    bestmonth = best_month(returns=returns)
    worstmonth = worst_month(returns=returns)
    bestyear = best_year(returns=returns)
    worstyear = worst_year(returns=returns)
    yearlymean = yearly_mean(returns=returns)
    yearlyvol = yearly_vol(returns=returns)
    yearlyskew = yearly_skew(returns=returns)
    yearly_kurt = yearly_kurtosis(returns=returns)
    avg_down_month = average_down_month(returns=returns)
    avg_up_month = average_up_month(returns=returns)
    win_year_perc = win_years_percent(returns=returns) * 100.0
    win_mo_perc = win_months_percent(returns=returns) * 100.0
    win_w_perc = win_weeks_percent(returns=returns) * 100.0

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
        'common_sense': cs,
        'win_loss_ratio': wlr,
        'cpc_index': cpc,
        'tail_ratio': tailr,
        'outlier_win_ratio': owr,
        'outlier_loss_ratio': olr,
        'start': start,
        'end': end,
        'years': ys,
        'total_return': tret,
        'cagr': cgr,
        'ytd': _ytd,
        'mtd': _mtd,
        'three_month': three_month,
        'six_month': six_month,
        'three_year': three_year,
        'daily_skew': dailyskew,
        'daily_kurt': daily_kurt,
        'best_day': bestday,
        'worst_day': worstday,
        'monthly_vol': monthlyvol,
        'monthly_skew': monthlyskew,
        'monthly_kurt': monthlykurt,
        'best_month': bestmonth,
        'worst_month': worstmonth,
        'best_year': bestyear,
        'worst_year': worstyear,
        'yearly_mean': yearlymean,
        'yearly_vol': yearlyvol,
        'yearly_skew': yearlyskew,
        'yearly_kurt': yearly_kurt,
        'avg_down_month': avg_down_month,
        'avg_up_month': avg_up_month,
        'win_year_perc': win_year_perc,
        'win_months_perc': win_mo_perc,
        'win_weeks_perc': win_w_perc
        }
