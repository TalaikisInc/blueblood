from os.path import join

from pandas_talib import (SMA, EMA, MOM, ROC, ATR, BBANDS, STOK, STO,
    TRIX, ADX, MACD, MassI, Vortex, KST, RSI, TSI, ACCDIST, PPSR,
    Chaikin, MFI, OBV, FORCE, EOM, CCI, COPP, KELCH, ULTOSC,
    DONCH, STDDEV)
from numpy import sqrt, sum, where, inf, nan
from pandas import concat

from app.data import get_pickle


def sma(data, per):
    return data.rolling(window=per, min_periods=per).mean()

# More: https://github.com/femtotrader/pandas_talib/blob/master/pandas_talib/__init__.py

def trigger(df):
    df['hc'] = df['High'] - df['Close']
    df['cl'] = df['Close'] - df['Low']
    df['range'] = where(df['hc'] >= df['cl'], df['hc'], df['cl'])
    return df['Close'].shift() - 0.5 * df['range']

def sumsq(df, per):
    df['diff'] = df['Close'] - sma(df, per)
    df['sq'] = df['diff'] * df['diff']
    df['sum'] = df['sq'].rolling(window=per, min_periods=per).sum()
    return df['sum']

def bbandWidthratio(df, dev, per):
    s = sumsq(df, per)
    sko = sqrt(s / per)
    return 2.0 * (dev * sko) / sma(df, per)

def keltner(df, const, per):
    df['mid'] = sma(df['Close'], per)
    df['avg'] = (df['High'] - df['Low']).rolling(window=per, min_periods=per).sum() / per
    df['upper'] = df['mid'] + const * df['avg']
    df['lower'] = df['mid'] - const * df['avg']
    return df

def gbtruerange(df, per, i):
   return (df['High'].iloc[-per+i:-per+i+1], df['Close'].iloc[-per+i-1:-per+i]).max() - (df['Low'].iloc[-per+i:-per+i+1], df['Close'].iloc[-per+i-1:-per]).min()

def ibs(df, sym):
    df['norm'] = df['{}_High'.format(sym)] - df['{}_Low'.format(sym)]
    return (df['{}_Close'.format(sym)] - df['{}_Low'.format(sym)]) / df['norm']

def rsi(df, sym, per):
    df['{}_Diff'.format(sym)] = df['{}_Close'.format(sym)].diff()
    df['up_sum'] = where(df['{}_Diff'.format(sym)] > 0, df['{}_Diff'.format(sym)], 0.0)
    df['dn_sum'] = where(df['{}_Diff'.format(sym)] <= 0, abs(df['{}_Diff'.format(sym)]), 0.0)
    df['gain'] = df['up_sum'].rolling(window=(per-1), min_periods=(per-1)).sum()
    df['loss'] = df['dn_sum'].rolling(window=(per-1), min_periods=(per-1)).sum()
    df['gain_sma'] = df['gain'].rolling(window=per, min_periods=per).mean()
    df['loss_sma'] = df['loss'].rolling(window=per, min_periods=per).mean()
    df['rel_sstr'] = 1.0 + df['gain_sma'] / df['loss_sma']
    return  (100.0 - 100.0 / df['rel_sstr'])

def bolinger(df, sym, per, dev):
    df['avg'] = df['{}_Close'.format(sym)].rolling(window=per, min_periods=per).mean()
    df['std'] = df['{}_Close'.format(sym)].rolling(window=per, min_periods=per).std()
    return (df['avg'] + df['std'] * dev), (df['avg'] - df['std'] * dev)

def sumsq(df, per):
    df['diff'] = df['Close'].diff()
    df['sq'] = df['diff'] * df['diff']
    df['sum'] = df['sq'].rolling(window=per, min_periods=per).sum()
    return df['sum']

def bbandWidthratio(df, dev, per):
    s = sumsq(df, per)
    sko = sqrt(s / per)
    return 2.0 * (dev * sko ) / df['Close'].shift()
