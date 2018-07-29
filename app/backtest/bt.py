from backtrader import Cerebro, Strategy, Order
from backtrader.analyzers import Returns

from app.data import get_pickle
from app.utils import read_parq
from app.data import PandasData


class StrategyFetcher(object):
    _STRATS = ['St0', 'St1']

    def __new__(cls, *args, **kwargs):
        idx = kwargs.pop('idx')

        obj = cls._STRATS[idx](*args, **kwargs)
        return obj

def run_bt_multiple():
    cerebro = Cerebro()
    df = get_pickle('tiingo', 'SPY')
    data = PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addanalyzer(Returns)
    cerebro.optstrategy(StrategyFetcher, idx=[0, 1])
    results = cerebro.run()

    strats = [x[0] for x in results]
    for i, strat in enumerate(strats):
        rets = strat.analyzers.returns.get_analysis()
        print('Strategy {} Name {}:\n  - analyzer: {}\n'.format(i, strat.__class__.__name__, rets))
