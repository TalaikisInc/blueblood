from alphalens.tears import (create_returns_tear_sheet, create_information_tear_sheet,
    create_turnover_tear_sheet, create_summary_tear_sheet, create_full_tear_sheet,
    create_event_returns_tear_sheet, create_event_study_tear_sheet)
from alphalens.utils import get_clean_factor_and_forward_returns

from data.local.readers import get_pickle


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

def run_analyze(factor):
    from importlib import import_module

    module_name = 'app.models.alpha.{}'.format(factor)
    imported_module = import_module(module_name, package='blueblood')

    SYMBOLS = ['EURUSD', 'SP500', 'BTCUSD', 'GOLD', 'CrudeOIL']
    PERIODS = [1440, 10080, 43200]
    for symbol in SYMBOLS:
        for period in PERIODS:
            data = get_pickle('mt', '{}_{}'.format(symbol, period))
            run_factor_analysis(factor=imported_module.compute(data), prices=data.CLOSE)
