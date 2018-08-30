from math import fsum

from scipy.stats import pearsonr

from backtrader.indicators import EMA, PeriodN
from backtrader import Indicator


class MACD(Indicator):
    lines = ('macd', 'signal', 'histo',)
    params = (
        ('period_me1', 12),
        ('period_me2', 26),
        ('period_signal', 9),
    )

    def __init__(self):
        me1 = EMA(self.data, period=self.p.period_me1)
        me2 = EMA(self.data, period=self.p.period_me2)
        self.l.macd = me1 - me2
        self.l.signal = EMA(self.l.macd, period=self.p.period_signal)
        self.l.histo = self.l.macd - self.l.signal

class PearsonR(PeriodN):
    _mindatas = 2

    lines = ('correlation',)
    params = (('period', 20),)

    def next(self):
        c, p = pearsonr(self.data0.get(size=self.p.period), self.data1.get(size=self.p.period))
        self.lines.correlation[0] = c

class ATR(Indicator):
    lines = ('atr',)
    params = (
        ('period', 20),
        ('ago', 1),
    )

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        hc1 = abs(self.data.high.get(self.p.ago, size=self.p.period) - self.data.close.get(self.p.ago+1, size=self.p.period))
        lc1 = abs(self.data.low.get(self.p.ago, size=self.p.period) - self.data.close.get(self.p.ago+1, size=self.p.period))
        hl = self.data.high.get(self.p.ago, size=self.p.period) - self.data.low.get(self.p.ago, size=self.p.period)
        self.lines.atr[0] = EMA(max(hc1, lc1, hl), period=self.p.period)

class MaxI(Indicator):
    lines = ('maxi',)
    plotinfo = {'plot': False, 'subplot': False}
    csv = True
    params = (
        ('period', 20),
        ('ago', 1),
    )

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        self.lines.maxi[0] = max(self.data.high.get(self.p.ago, size=self.p.period))

class MinI(Indicator):
    lines = ('mini',)
    plotinfo = {'plot': False, 'subplot': False}
    csv = True
    params = (
        ('period', 20),
        ('ago', 1),
    )

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        self.lines.mini[0] = min(self.data.low.get(self.p.ago, size=self.p.period))

class Swing(Indicator):
    '''
    A Simple swing indicator that measures swings (the lowest/highest value)
    within a given time period.
    '''
    lines = ('swings', 'signal')
    params = (('period', 7),)
    plotinfo = {'plot': True, 'subplot': False}
    csv = True

    def __init__(self):
        #Set the swing range - The number of bars before and after the swing
        #needed to identify a swing
        self.swing_range = (self.p.period * 2) + 1
        self.addminperiod(self.swing_range)

    def next(self):
        #Get the highs/lows for the period
        highs = self.data.high.get(size=self.swing_range)
        lows = self.data.low.get(size=self.swing_range)
        #check the bar in the middle of the range and check if greater than rest
        if highs.pop(self.p.period) > max(highs):
            self.lines.swings[-self.p.period] = 1 #add new swing
            self.lines.signal[0] = 1 #give a signal
        elif lows.pop(self.p.period) < min(lows):
            self.lines.swings[-self.p.period] = -1 #add new swing
            self.lines.signal[0] = -1 #give a signal
        else:
            self.lines.swings[-self.p.period] = 0
            self.lines.signal[0] = 0
