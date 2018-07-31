from os.path import join

from numpy import isinf, isnan, nan
from clint.textui import colored
from pandas import read_pickle, read_csv, to_datetime, TimeGrouper
from fastparquet import ParquetFile
from stopwatch import StopWatch, format_report
sw = StopWatch()

from backtrader import TimeFrame
from app.utils import STORAGE_PATH, filenames
from .mt import get_mt, META_PATH
from backtrader.feeds import GenericCSVData


def fill_forward(data):
    ''' Fills forward empty data spots. '''
    return data.fillna(method='ffill')

def get_pickle(folder, name):
    df = read_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))
    df.index = to_datetime(df.index)
    return df

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

def get_csv(folder, name, skip=False):
    if skip:
        df = read_csv(join(STORAGE_PATH, folder, '{}.csv'.format(name)), parse_dates=[0], skiprows=1)
    else:
        df = read_csv(join(STORAGE_PATH, folder, '{}.csv'.format(name)), parse_dates=[0])
    df.sort_index(axis=0, ascending=True, inplace=True)
    return df

def chunkize_df_years(df, freq='Y'):
    ''' Slice DataFrame into years. '''
    df = df.set_index('Time')
    return df.groupby(TimeGrouper(freq=freq))

def chunkize_df(df):
    ''' Slice DataFrame into smaller chunks. '''
    n = 1000000
    return [df[i:i+n] for i in range(0, df.shape[0], n)]

def read_bt_csv(folder, symbol, ticks=True):
    if ticks:
        data = GenericCSVData(dataname=join(STORAGE_PATH, folder, '{}.csv'.format(symbol)),
            nullvalue=0.0,
            dtformat='%Y-%m-%d %H:%M:%S.%f',
            tmformat='%H:%M:%S.%f',
            datetime=0,
            time=-1,
            open=1,
            high=1,
            low=1,
            close=1,
            volume=3,
            openinterest=-1,
            timeframe=TimeFrame.Ticks)
    else:
        data = GenericCSVData(dataname=join(STORAGE_PATH, folder, '{}.csv'.format(symbol)),
            nullvalue=0.0,
            dtformat='%Y-%m-%d',
            # tmformat='%H:%M:%S.%f',
            datetime=0,
            time=-1,
            open=1,
            high=2,
            low=3,
            close=4,
            volume=5,
            openinterest=-1,
            timeframe=TimeFrame.Days)
    return data

def split_ticks(folder, symbol, years=False):
    ''' Splits big DataFrame into chunks and saves to disk. '''
    df = get_csv(folder=folder, name=symbol)
    if years:
        dfs = chunkize_df_years(df=df)
    else:
        dfs = chunkize_df(df=df)
    for i, chunk in enumerate(dfs):
        chunk = chunk.set_index('Time')
        chunk.to_csv(join(STORAGE_PATH, folder, '_split', '{}_{}.csv'.format(symbol, i)))
