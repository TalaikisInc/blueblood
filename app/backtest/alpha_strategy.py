from numpy import where, percentile, sqrt
from matplotlib import pyplot as plt
from clint.textui import colored

from app.data.local import get_pickle, transform_multi_data, join_data
from app.models.alpha import all_alphas, alpha
from app.stats import clean_prices, clean_alpha, percentiles, sharpe_ratio
from app.utils import DATA_SOURCE
from app.variables import BASKETS


def sharpe(df, s):
    return sharpe_ratio(returns=df['{}_ret'.format(s)], rf=0.00) * sqrt(252)

def no_perc(df, symbols):
    for s in symbols:
        df['{}_ret'.format(s)] = where(df[s].shift() < 0, df['{}_Pct'.format(s)], 0)
        plt.plot(df['{}_ret'.format(s)].cumsum())
    plt.show()

def run_factor(data, model, BASKET):
    df = alpha(model=int(model), symbols=BASKET, train=True)
    df = clean_alpha(data=df, symbols=BASKET, d_type='eod_strategy')
    df = df.dropna()
    no_perc(df=df, symbols=BASKET)
    for t in range(2):
        for i in [50, 10, 90]:
            print(colored.green('Percentile %s' % i))
            def p(x, i=i):
                return percentile(x, i)
            for s in BASKET:
                print(s)
                df['{}_p'.format(s)] = df[s].rolling(window=100, min_periods=100).apply(p)
                if t == 1:
                    print('Long short')
                    df['{}_ret'.format(s)] = where(df[s].shift() < df['{}_p'.format(s)].shift(), df['{}_Pct'.format(s)], -df['{}_Pct'.format(s)])
                else:
                    print('Long')
                    df['{}_ret'.format(s)] = where(df[s].shift() < df['{}_p'.format(s)].shift(), df['{}_Pct'.format(s)], 0)
                print('Sharpe: %s' % sharpe(df, s) )
                plt.plot(df['{}_ret'.format(s)].cumsum())
            plt.show()

def run_alpha_strategy(model):
    try:
        model = int(model)
    except:
        model = None
        pass
    BASKET = BASKETS[1].symbols

    initial = get_pickle(DATA_SOURCE, BASKET[0])
    initial = transform_multi_data(data=initial, symbol=BASKET[0])
    data = join_data(primary=initial, folder=DATA_SOURCE, symbols=BASKET[1:])
    data = clean_prices(data=data, symbols=BASKET, d_type='eod')

    if model is None:
        for i in all_alphas():
            print('Alpha %s' % i)
            run_factor(data, i, BASKET)
    else:
        run_factor(data, model, BASKET)
