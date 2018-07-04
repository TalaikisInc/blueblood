from numpy import log, sqrt, exp
from scipy.stats import norm


def d1(S0, K, r, sigma, T):
    return (log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * sqrt(T))
 
def d2(S0, K, r, sigma, T):
    return (log(S0 / K) + (r - sigma**2 / 2) * T) / (sigma * sqrt(T))
 
def BlackScholes(type,S0, K, r, sigma, T):
    if type=="C":
        return S0 * norm.cdf(d1(S0, K, r, sigma, T)) - K * exp(-r * T) * norm.cdf(d2(S0, K, r, sigma, T))
    else:
       return K * exp(-r * T) * norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * norm.cdf(-d1(S0, K, r, sigma, T))


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
