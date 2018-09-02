from importlib import import_module
from os.path import dirname, join

from matplotlib import pyplot
from clint.textui import colored
from pandas import concat, DataFrame

from app.utils import save_port, save_tradeable
from app.utils.file_utils import filenames
from app.data import get_pickle
from app.stats import stats_printout
from app.plot import drawdown, drawdown_to_percentile


def generate_portfolios():
    printout = False
    plot = False
    fs = filenames(join(dirname(__file__), '_implementations'))

    for f in fs:
        print('Generating portfolio from %s' % f)
        try:
            module_name = 'app.portfolio._implementations.{}'.format(f.split('.')[0])
            imported_module = import_module(module_name, package='blueblood')
            for i in imported_module.main():
                market = get_pickle('tiingo', 'SPY')['SPY_AdjClose'].pct_change()

                df = concat([i[0], i[1], i[2], market], axis=1)
                df.columns = ['returns', 'adj_returns', 'comm', 'market']
                save_tradeable(i[4], i[3])
                save_port(data=df, name=i[3])

                if printout:
                    stats_printout(returns=df['adj_returns'], market=df['market'])

                if plot:
                    final_sum = df['adj_returns'].cumsum()
                    market_sum = df['market'].cumsum()
                    final_sum.plot()
                    market_sum.plot()
                    plt.show()
                    drawdown(final_sum)
                    drawdown_to_percentile(final_sum)
                print(colored.green('Saved portfolio %s' % i[3]))
        except Exception as err:
            print(colored.red(err))
