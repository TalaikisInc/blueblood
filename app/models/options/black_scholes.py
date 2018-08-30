from datetime import datetime
from numpy import log, sqrt, exp
from scipy.stats import norm

n = norm.pdf
N = norm.cdf

def d1(S0, K, r, sigma, T):
    return (log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
 
def d2(S0, K, r, sigma, T):
    return (log(S0 / K) + (r - sigma**2 / 2) * T) / (sigma * sqrt(T))
 
def BlackScholes(type,S0, K, r, sigma, T):
    if type=="C":
        return S0 * norm.cdf(d1(S0, K, r, sigma, T)) - K * exp(-r * T) * norm.cdf(d2(S0, K, r, sigma, T))
    else:
       return K * exp(-r * T) * norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * norm.cdf(-d1(S0, K, r, sigma, T))

def bs_price(cp_flag, S, K, T, r, v, q=0.0):
    d1 = (log(S / K) + (r + v * v / 2.) * T) / (v * sqrt(T))
    d2 = d1 - v * sqrt(T)
    if cp_flag == 'c':
        price = S*exp(-q*T) * N(d1)-K*exp(-r*T) * N(d2)
    else:
        price = K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)
    return price

def bs_vega(cp_flag, S, K, T, r, v, q=0.0):
    d1 = (log(S / K) + (r + v * v / 2.) * T) / (v * sqrt(T))
    return S * sqrt(T) * n(d1)

def example():
    """
    r - continuously compounded risk-free rate
    sigma - annualized volatility
    T - maturity, in years
    S0 - stock price
    K - strike
    returns price
    """
    bs = BlackScholes(type="C", S0=100, K=100, r=0.05, sigma=0.1, T=1/12)
    print(bs)

def find_vol(target_value, call_put, S, K, T, r):
    MAX_ITERATIONS = 100
    PRECISION = 1.0e-5

    sigma = 0.5
    for i in xrange(0, MAX_ITERATIONS):
        price = bs_price(call_put, S, K, T, r, sigma)
        vega = bs_vega(call_put, S, K, T, r, sigma)

        price = price
        diff = target_value - price  # our root

        print(i, sigma, diff)

        if (abs(diff) < PRECISION):
            return sigma
        sigma = sigma + diff/vega # f(x) / f'(x)

    # value wasn't found, return best guess so far
    return sigma

def implied_volatility():
    V_market = 17.5
    K = 585
    T = (datetime.date(2014,10,18) - datetime.date(2014,9,8)).days / 365.
    S = 586.08
    r = 0.0002
    cp = 'c' # call option

    implied_vol = find_vol(V_market, cp, S, K, T, r)

    print('Implied vol: %.2f%%' % (implied_vol * 100))
