from numpy import where
from matplotlib import pyplot as plt

from data.local import get_pickle, transform_multi_data, join_data
from models.alpha import all_alphas, alpha
from .functions import clean_prices, clean_alpha, transform_for_analysis
from utils import DATA_SOURCE
from .index import percentiles


def run_factor(data, model, BASKET):
    df = alpha(model=int(model), symbols=BASKET, train=True)
    df = clean_alpha(data=df, symbols=BASKET, d_type='eod_strategy')
    # df = transform_for_analysis(df)
    df = df.dropna()
    for s in BASKET:
        p = percentiles(returns=df[s].dropna())
        df['{}_ret'.format(s)] = where(df['{}'.format(s)] < p[50], df['{}_Pct'.format(s)], 0)
        plt.plot(df['{}_ret'.format(s)].cumsum())
    plt.show()

def run_strategy(model):
    try:
        model = int(model)
    except:
        model = None
        pass

    BASKET = ['QQQ', 'SPY', 'IWM', 'EEM', 'TLT']

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
