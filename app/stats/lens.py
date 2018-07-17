from pandas import DatetimeIndex, DataFrame, MultiIndex
from matplotlib import pyplot as plt

from .alphalens.tears import (create_returns_tear_sheet, create_information_tear_sheet,
    create_turnover_tear_sheet, create_summary_tear_sheet, create_full_tear_sheet,
    create_event_returns_tear_sheet, create_event_study_tear_sheet)
from .alphalens.utils import get_clean_factor_and_forward_returns
from data.local import get_pickle, transform_multi_data, join_data
from models.alpha import all_alphas, alpha


def run_factor_analysis(factor, prices):
    factor_data = get_clean_factor_and_forward_returns(factor, prices, quantiles=5)
    create_full_tear_sheet(factor_data)

def run_event_analsyis(event, prices):
    factor_data = get_clean_factor_and_forward_returns(event, prices, quantiles=None, bins=1,
        periods=(1, 2, 3, 4, 5, 10, 15), filter_zscore=None)
    create_full_tear_sheet(factor_data)
    return factor_data

def event_distribution(event, prices):
    create_event_study_tear_sheet(run_event_analsyis(event=event, prices=prices), prices, avgretplot=(5, 10))

def clean_alpha(data, symbols):
    for s in symbols:
        data = data.drop([
            '{}_Open'.format(s),
            '{}_High'.format(s),
            '{}_Low'.format(s),
            '{}_Close'.format(s),
            '{}_Volume'.format(s),
            '{}_Div'.format(s),
            '{}_Split'.format(s),
            '{}_AdjClose'.format(s)
        ], axis=1)
    return data.dropna()

def clean_prices(data, symbols):
    for s in symbols:
        data = data.drop([
            '{}_Open'.format(s),
            '{}_High'.format(s),
            '{}_Low'.format(s),
            '{}_Volume'.format(s),
            '{}_Div'.format(s),
            '{}_Split'.format(s),
            '{}_AdjClose'.format(s)
        ], axis=1)
        data.rename(columns={ '{}_Close'.format(s): s}, inplace=True)
    return data

def run(model, BASKET):
    initial = get_pickle('accepted', BASKET[0])
    initial = transform_multi_data(data=initial, symbol=BASKET[0])
    data = join_data(primary=initial, folder='accepted', symbols=BASKET[1:])
    data = clean_prices(data, BASKET)

    a = alpha(model=int(model), symbols=BASKET, train=True)
    a = clean_alpha(a, BASKET)
    #plt.scatter(a['GOOGL'].dropna().shift(), a['GOOGL_Diff'].dropna())
    #plt.show()
    df = DataFrame(a.dropna().stack(), index=MultiIndex.from_product([a.index, a.columns], names=['date', 'symbol']))
    run_factor_analysis(factor=df, prices=data.dropna())

def run_analyze(model):
    try:
        model = int(model)
    except:
        model = None
        pass
    BASKET = ['AAPL', 'ABR', 'EEM', 'AMZN', 'GLD', 'GOOGL', 'BAC', 'CSCO', 'MSFT']

    if model is None:
        for i in all_alphas():
            print('Alpha %s' % i)
            run(i, BASKET)
    else:
        run(model, BASKET)
