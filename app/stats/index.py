from numpy import (cov, std, array, matrix, abs, mean, empty, sort, empty, sum, sqrt,
    power, maximum, round, where, percentile, busday_count)
import scipy.stats as sc
from pandas import to_datetime

from app.utils import periodize_returns, comm, quantity, PER_SAHRE_COM, FINRA_FEE, SEC_FEE
from app.db import Strategy, Stats


def max_dd(drawdowns):
    return abs(drawdowns.min())

def beta(returns, benchmark):
    m = benchmark.values
    s = returns.values
    covariance = cov(s, m)
    beta = covariance[0, 1] / covariance[1, 1]
    return beta

def vol(returns):
    return std(returns)

def treynor(returns, benchmark, rf):
    return (returns.mean() - rf) / beta(returns, benchmark)
  
def sharpe_ratio(returns, rf):
    if vol(returns) != 0:
        return (returns.mean() - rf) / vol(returns)
    else:
        return 0

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
    diff = diff.clip()
    return sum(diff ** order) / len(returns)
 
def hpm(returns, threshold, order):
    threshold_array = empty(len(returns))
    threshold_array.fill(threshold)
    diff = returns - threshold_array
    diff = diff.clip()
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
    return (returns.mean() - rf) / power(lpm(returns=returns, threshold=target, order=3), 1/3.0)

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

def sterling_ration(returns, rf):
    add = average_dd(returns.cumsum())
    if add > 0:
        return (returns.mean() - rf) / add
    else:
        return None

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


def commissions(df, symbol, com=None):
    capital = 100000
    if com is None:
        com = PER_SAHRE_COM + FINRA_FEE
    df['quantities'] = quantity(capital=capital, price=df['{}_Close'.format(symbol)], alloc=1.0)
    df['c'] = comm(q=df['quantities'], p=com) + SEC_FEE / (1000000 / capital)

    df['com'] = where((df['sig'] == 0) & (df['sig'].shift() == 1), df['c'], 0)
    df['com'] += where((df['sig'] == 1) & (df['sig'].shift() == 0), df['c'], 0)
    df['com'] += where((df['sig'] == 0) & (df['sig'].shift() == -1), df['c'], 0)
    df['com'] += where((df['sig'] == -1) & (df['sig'].shift() == 0), df['c'], 0)
    df['com'] += where((df['sig'] == 1) & (df['sig'].shift() == -1), df['c'], 0)
    df['com'] += where((df['sig'] == -1) & (df['sig'].shift() == 1), df['c'], 0)
    return df['com'], (df['com'] / capital), df['quantities']

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
    return sum(where(returns < 0, 1, 0))

def win_rate(returns):
    return total_wins(returns) / len(returns)

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

TARGET = 0.05
RF = 0.05
ALPHA = 0.05

def run_stats():
    for strategy in Strategy.select():
        returns = DataFrame() # READ RETURNS HERE
        data = DataFrame()  # READ OHLC HERE
        benchmark = DataFrame()  # READ BENCHMARK
        signals = DataFrame() # READ SIGNALS
        pos = strategy.rule
        cumulative = returns.cumsum()
        perf = data['Close'].calc_stats()
        stats = perf.stats

        ma = mae(high=data['High'], low=data['Low'], close=data['Close'], pos=pos)
        mf = mae(high=data['High'], low=data['Low'], close=data['Close'], pos=pos)
        b = beta(returns=returns, benchmark=benchmark)
        Stats.create(
            strategy=strategy,
            max_dd=max_dd(drawdowns=drawdowns(cumulative=cumulative)),
            beta=b,
            vol=vol(returns=returns),
            treynor=treynor(returns=returns, benchmark=benchmark, rf=RF),
            sharpe_ratio=sharpe_ratio(returns=returns, rf=RF),
            ir=ir(returns=returns, benchmark=benchmark),
            modigliani=modigliani(returns=returns, benchmark=benchmark, rf=RF),
            var=var(returns=returns, alpha=ALPHA),
            cvar=cvar(returns=returns, alpha=ALPHA),
            excess_var=excess_var(returns=returns, rf=RF, alpha=ALPHA),
            conditional_sharpe=conditional_sharpe(returns=returns, rf=RF, alpha=ALPHA),
            omega_ratio=omega_ratio(returns=returns, rf=RF, target=TARGET),
            sortino=sortino(returns=returns, rf=RF, target=TARGET),
            kappa_three=kappa_three(returns=returns, rf=RF, target=TARGET),
            gain_loss=gain_loss(returns=returns, target=TARGET),
            upside_potential=upside_potential(returns=returns, target=TARGET),
            calmar=calmar(returns=returns, rf=RF),
            average_dd=average_dd(cumulative=cumulative),
            average_dd_squared=average_dd_squared(cumulative=cumulative),
            sterling_ration=sterling_ration(returns=returns, rf=RF),
            burke_ratio=burke_ratio(returns=returns, cumulative=cumulative, rf=RF),
            average_month_return=average_month_return(returns=returns),
            average_trades_month=average_trades_month(signals=signals, retruns=retruns),
            average_dd_duration=average_dd_duration(cumulative=cumulative),
            max_dd_duration=max_dd_duration(cumulative=cumulative),
            trade_count=trade_count(signals=signals),
            alpha=alpha(portfolio_return=returns, rf=rf, beta=b, market_return=benchmark),
            average_trade=average_trade(returns=returns),
            average_win=average_win(returns=returns),
            average_loss=average_loss(returns=returns),
            total_wins=total_wins(returns=returns),
            total_losses=total_losses(returns=returns),
            win_rate=win_rate(returns=returns),
            # @TODO thos two should show only on trade days:
            average_mae=average_mae(high=data['High'], low=data['Low'], close=data['Close'], pos=pos),
            average_mfe=average_mfe(high=data['High'], low=data['Low'], close=data['Close'], pos=pos),
            max_mae=max_mae(cumulative=cumulative, mae=ma),
            min_mfe=min_mfe(cumulative=cumulative, mfe=mf),
            ulcer_index=ulcer_index(cumulative=cumulative),
            ulcer_performance_index=ulcer_performance_index(cumulative=cumulative, r=returns.mean(), rf=rf),
            start=stats['start'],
            end=stats['end'],
            total_return=stats['total_return'],
            daily_sharpe=stats['daily_sharpe'],
            cagr=stats['cagr'],
            mtd=stats['mtd'],
            three_month=stats['three_month'],
            six_month=stats['six_month'],
            ytd=stats['ytd'],
            three_year=stats['three_year'],
            daily_mean=stats['daily_mean'],
            daily_vol=stats['daily_vol'],
            daily_skew=stats['daily_skew'],
            daily_kurt=stats['daily_kurt'],
            best_day=stats['best_day'],
            worst_day=stats['worst_day'],
            monthly_sharpe=stats['monthly_sharpe'],
            monthly_mean=stats['monthly_mean'],
            monthly_vol=stats['monthly_vol'],
            monthly_skew=stats['monthly_skew'],
            monthly_kurt=stats['monthly_kurt'],
            best_month=stats['best_month'],
            worst_month=stats['worst_month'],
            yearly_sharpe=stats['yearly_sharpe'],
            yearly_mean=stats['yearly_mean'],
            yearly_vol=stats['yearly_vol'],
            yearly_skew=stats['yearly_skew'],
            yearly_kurt=stats['yearly_kurt'],
            worst_year=stats['worst_year'],
            avg_drawdown_days=stats['avg_drawdown_days'],
            avg_up_month=stats['avg_up_month'],
            avg_down_month=stats['avg_down_month'],
            win_year_perc=stats['win_year_perc'],
            twelve_month_win_perc=stats['twelve_month_win_perc']
        )
"""
            capital_utilization=
            rolling_sharpe=
            returns_by_month=
            returns_by_year=
            percentiles=
            drawdown_probability=
            return_probability=
"""

STAT_MAP = {
    'beta': 'Measure of the risk arising from exposure to general market, a.k.a. systemic risk.',
    'vol': 'Variability.',
    'treynor': 'Relates excess return over the risk-free rate to the additional systematic() risk taken.',
    'sharpe_ratio': 'Reward-to-variability ratio is a way to examine the performance by adjusting for its risk (variability in this case).',
    'ir': 'The information ratio is often used to gauge the skill of managers of mutual funds, hedge funds, etc. In this case, it measures the active return of the manager\'s portfolio divided by the amount of risk that the manager takes relative to the benchmark.',
    'modigliani': 'It measures the returns of the portfolio, adjusted for the risk of the portfolio relative to that of some benchmark.',
    'var': 'Value at risk, probability of occurrence for the defined loss.',
    'cvar': 'Conditional VaR, also known as mean excess loss, mean shortfall, tail value at risk, average value at risk or expected shortfall.',
    'conditional_sharpe': 'The ratio of expected excess return to the expected shortfall.',
    'omega_ratio': 'Probability weighted ratio of gains versus losses for threshold return target ({}).'.format(TARGET),
    'sortino': 'It is a modification of the Sharpe ratio that penalizes only those returns falling below a target ({}) and required rate of return ({}).'.format(TARGET, RF),
    'kappa_three': 'Omega and the Sortino ratio are two among many potential variants of Kappa. In certaincircumstances, other Kappa variants may be more appropriate or provide more powerful insights.',
    'upside_potential': 'A measure of a return relative to the minimal acceptable return.',
    'calmar': 'The Calmar ratio changes gradually and serves to smooth out the overachievement and underachievement periods of performance more readily than either the Sterling or Sharpe ratios.',
    'sterling_ration': 'Measures return over average drawdown.',
    'burke_ratio': 'Similar to the Sterling ratio, the Burke ratio discounts the expected excess return of the security by the square root of the average of the worst expected maximum drawdowns squared for the portfolio.',
    'alpha': 'This is based on the concept that riskier assets should have higher expected returns than less risky assets. If an asset\'s return is higher than the risk adjusted return, that asset is said to have \'positive alpha\' or \'abnormal returns\'.',
    'average_mae': 'Average adverse excursion.',
    'average_mfe': 'Average favorable excursion.',
    'max_mae': 'Maximum adverse excursion.',
    'min_mfe': 'Minimum of favorable excursion.',
    'ulcer_index': 'Ulcer Index measures downside risk, in terms of both depth and duration of price declines.',
    'ulcer_performance_index': 'Ulcer Performance Index, a.k.a. Martin ratio is a Sharpe ratio with Ulcer Index instead of variability.'
}

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

def stats_printout(returns, market):
    c = returns.cumsum()

    print('Basics -----------------------')
    vv = vol(returns=returns)
    print('Volatility %.3f%%' % (vv * 100.0))
    amr = average_month_return(returns=returns) * 100.0
    print('Average month return %.3f%%' % amr)
    # trade_count(signals)
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
    print('Sharpe* %.3f' % (sharpe_ratio(returns, rf=0.0) * sqrt(252)))
    b = beta(returns=returns, benchmark=market)
    print('Beta %.3f' % b)
    a = alpha(portfolio_return=returns.mean(), rf=0.0, beta=b, market_return=market.mean())
    print('Alpha %.3f' % a)
    tr = treynor(returns=returns, benchmark=market, rf=0.0)
    print('Treynor %.3f' % tr)
    infr = ir(returns=returns, benchmark=market)
    print('Information ratio %.3f' % infr)
    mod = modigliani(returns=returns, benchmark=market, rf=0.0)
    print('Modigliani ratio %.3f' % mod)
    ora = omega_ratio(returns=returns, rf=0.0, target=0.0)
    print('Omega Ratio %.3f' % ora)
    so = sortino(returns=returns, rf=0.0, target=0)
    print('Sortino Ratio %.3f' % so)
    kt = kappa_three(returns=returns, rf=0.0, target=0.05)
    print('Kappa Three %.3f' % kt)
    up = upside_potential(returns=returns, target=0.0)
    print('Upside potential ratio %.3f' % up)
    cal = calmar(returns=returns, rf=0.0)
    print('Calmar Ratio %.3f' % cal)
    ui = ulcer_index(cumulative=c)
    print('Ulcer Index %.3f' % ui)
    upi = ulcer_performance_index(cumulative=c, r=returns.mean(), rf=0.0)
    print('Ulcer Performance Index %.3f' % upi)
    stra = sterling_ration(returns=returns, rf=0.0)
    if stra is not None:
        print('Sterling Ratio %.3f' % stra)
    br = burke_ratio(returns=returns, cumulative=c, rf=0.0)
    print('Burke Ratio %.3f' % br)

    print()
    print('VaR --------------------------')
    v = var(returns=returns, alpha=a)
    print('VaR %.3f' % v)
    cvv = cvar(returns=returns, alpha=a)
    print('Conditional VaR %.3f' % cvv)
    ev = excess_var(returns=returns, rf=0.0, alpha=a)
    print('Excess VaR %.3f' % ev)
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

    #mae(high, low, close, pos=0)
    #mfe(high, low, close, pos=0)
    #max_mae(cumulative, mae)
    #min_mfe(cumulative, mfe)
    #average_mae(high, low, close, pos=0)
    #average_mfe(high, low, close, pos=0)

    print('* Values are annualized.')

def stats_values(returns, market):
    c = returns.cumsum()
    vv = vol(returns=returns) * 100.0
    amr = average_month_return(returns=returns) * 100.0
    # trade_count(signals)
    at = average_trade(returns=returns) * 100.0
    aw = average_win(returns=returns) * 100.0
    al = average_loss(returns=returns) * 100.0
    w = total_wins(returns=returns)
    l = total_losses(returns=returns)
    wr = win_rate(returns=returns) * 100.0
    acor = correlation(returns=returns)
    sr = sharpe_ratio(returns, rf=0.0) * sqrt(252)
    b = beta(returns=returns, benchmark=market)
    a = alpha(portfolio_return=returns.mean(), rf=0.0, beta=b, market_return=market.mean())
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
    #mae(high, low, close, pos=0)
    #mfe(high, low, close, pos=0)
    #max_mae(cumulative, mae)
    #min_mfe(cumulative, mfe)
    #average_mae(high, low, close, pos=0)
    #average_mfe(high, low, close, pos=0)

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
        }
