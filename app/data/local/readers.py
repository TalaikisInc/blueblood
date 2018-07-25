from os.path import join

from numpy import isinf, isnan, nan
from clint.textui import colored
from pandas import read_pickle, read_csv
from fastparquet import ParquetFile
from stopwatch import StopWatch, format_report
sw = StopWatch()

from app.utils import STORAGE_PATH
from .mt import get_mt, META_PATH
from app.utils import filenames

def fill_forward(data):
    ''' Fills forward empty data spots. '''
    return data.fillna(method='ffill')

def get_pickle(folder, name):
    return read_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))

def get_parquet(name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    pf = ParquetFile(path)
    return pf.to_pandas()

def transform_multi_data(data, symbol):
    ''' Changes column names into differentiable ones. '''
    for col in data.columns:
        data['{}_{}'.format(symbol, col)] = data[col]
        data = data.drop([col], axis=1)
    return data

def normalize(folder, data):
    ''' Make coilumn names same as other dfs.'''
    if folder == 'tiingo':
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume', 'adjClose': 'Adjusted_close'}, inplace=True)
    return data

def clean(folder, data):
    ''' Clens not needed and data errors.'''
    if folder == 'fred':
        data = data.drop(['realtime_start'], axis=1)
    if folder == 'eod':
        data = data.drop(['Open', 'High', 'Low', 'Volume', 'Adjusted_close'], axis=1)
    if len(data.loc[data['Close'] == 0]) > 0:
        return None
    assert len(data.loc[data['Close'] == 0]) == 0, 'Data has zeros!'
    assert len(data.index[isinf(data).any(1)]) == 0, 'Data has inf!'
    assert len(data.index[isnan(data).any(1)]) == 0, 'Data has nan!'
    return data

def join_data(primary, folder, symbols, clr=False):
    ''' Makes one DataFrame for many symbols. '''
    with sw.timer('join_data'):
        for symbol in symbols:
            data = get_pickle(folder, symbol).dropna()
            data = normalize(folder, data)
            if clr:
                data = clean(folder=folder, data=data)
            if data is not None:
                data = transform_multi_data(data=data, symbol=symbol)
                primary = primary.join(data, how='left')
        d = fill_forward(data=primary)
    print(format_report(sw.get_last_aggregated_report()))
    return d

def convert_mt_pickle():
    ''' Converts MT4 exported CSV to lcoal format. '''
    fs = filenames(META_PATH)
    for f in fs:
        try:
            name = f.split('_')[3]
            per = f.split('_')[4].split('.')[0]
            dest_path = join(STORAGE_PATH, 'mt', '{}_{}.p'.format(name, per))
            data = get_mt(name, per)
            if len(data) > 500:
                data.rename(columns={'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
                data.to_pickle(dest_path)
                print(colored.green('Converted for {} {}'.format(name, per)))
        except Exception as err:
            print(colored.red(err))

def get_csv(folder, name):
    df = read_csv(join(STORAGE_PATH, folder, '{}.csv'.format(name)), parse_dates=[0])
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df
