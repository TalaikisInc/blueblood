from bt import Strategy, Backtest, run
from bt.algos import (RunMonthly, RunOnce, RunPeriod, RunDaily, RunWeekly, RunQuarterly,
    RunYearly, RunOnDate, RunAfterDate, RunAfterDays, RunEveryNPeriods)
from bt.algos import (SelectAll, SelectThese, SelectHasData, SelectN, SelectMomentum,
    SelectWhere, SelectRandomly, StatTotalReturn)
from bt.algos import (WeighEqually, WeighSpecified, WeighTarget, WeighInvVol,
    WeighERC, WeighMeanVar, WeighRandomly)
from bt.algos import (Rebalance, LimitDeltas, LimitWeights, CapitalFlow, CloseDead,
    RebalanceOverTime)
from pandas import DateOffset
from matplotlib import pyplot as plt

from data.local import get_pickle
from utils import train_test_split, join_data
from models.alpha import alpha


def commissions(q, p):
    return abs(q) * 0.01

def res(s, data):
    test = Backtest(s, data, commissions=commissions)
    res = run(test)
    res.display()
    res.plot()
    plt.show()

def basic_runs():
    # @TODO abstract this idiocy:
    SYMBOLS = ['SP500_1440', 'NASDAQ100_1440', 'RUSSELL2000_1440', 'DAX30_1440',
        'FTSE100_1440', 'DJ30_1440', '10YTNOTES_1440', 'GOLD_1440', 'OMX30_1440',
        'NIFTY50_1440', 'CAC40_1440']
    initial = get_pickle('mt', SYMBOLS[0])
    del initial['Open']
    del initial['High']
    del initial['Low']
    del initial['Volume']
    initial.columns = ['SP500_1440']
    initial = join_data(primary=initial, folder='mt', factors=SYMBOLS[1:])
    initial = initial.dropna()
    data, test = train_test_split(data=initial, part=0.6)

    s = Strategy('s2', [RunDaily(), SelectWhere(alpha(data) < 8), WeighEqually(), Rebalance()])
    res(s, data)
