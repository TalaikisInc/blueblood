from ffn import calc_prob_mom
from numpy import sqrt


def prob_momentum(returns_a, returns_b):
    return calc_prob_mom(returns_a, returns_b)

def i13612W(df, col):
    tmp = df[col].copy()
    tmp = tmp.pct_change().resample('1M').sum()

    tmp1 = tmp.rolling(window=1, min_periods=1).mean() * sqrt(252)
    tmp3 = tmp.rolling(window=3, min_periods=3).mean() * sqrt(252)
    tmp6 = tmp.rolling(window=6, min_periods=6).mean() * sqrt(252)
    tmp12 = tmp.rolling(window=12, min_periods=12).mean() * sqrt(252)
    tmp = (tmp1 + tmp3 + tmp6 + tmp12) / 4
    tmp = tmp.resample('1D').ffill()
    return tmp
