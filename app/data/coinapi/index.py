from os import getenv

from pandas import DataFrame
from coinapi_v1 import CoinAPIv1

from app.data import get_pickle, to_pickle


def coinapi_exchanges(api):
    exchanges = DataFrame(api.metadata_list_exchanges())
    to_pickle(exchanges, 'coinapi', 'exchanges')

def coinapi_coins(api):
    symbols = DataFrame(api.metadata_list_symbols())
    to_pickle(symbols, 'coinapi', 'symbols')

def coinapi_periods(api):
    periods = DataFrame(api.ohlcv_list_all_periods())
    to_pickle(periods, 'coinapi', 'periods')

def conapi_data(api, symbol_id, period, start_data):
    data = DataFrame(
        api.ohlcv_historical_data('{}'.format(symbol_id), {'period_id': period, 'time_start': start_data})
    )
    to_pickle(data, 'coinapi', 'symbols', '{}_{}'.format(symbol_id, period))

def coinapi_save_initial_data(api):
    coinapi_exchanges(api)
    coinapi_coins(api=api)
    coinapi_periods(api=api)

def coinapi_collect_all_coins(api):
    coins = get_pickle('coinapi', 'symbols')
    filtered_coins = coins.loc[coins['symbol_type'] == 'SPOT'].loc[coins['exchange_id'] == 'BITTREX'].reset_index()
    for i in range(0, len(filtered_coins)):
        d = filtered_coins.ix[i]['data_start'].split('-')
        start_data = date(int(d[0]), int(d[1]), int(d[2])).isoformat()
        conapi_data(api=api, symbol_id=filtered_coins.ix[i]['symbol_id'], period='1HRS', start_data=start_data)
        print('{}/{}'.format(i, len(filtered_coins)))

def main():
    api = CoinAPIv1(getenv('COINAPI_API_KEY'))
    coinapi_collect_all_coins(api=api)
