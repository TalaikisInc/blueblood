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

def normalize(folder, data):
    ''' Make coilumn names same accross different data sources.'''
    if folder == 'eod':
        data.rename(columns={'Adjusted_close': 'AdjClose'}, inplace=True)
    if folder == 'tiingo':
        data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume', 'adjClose': 'AdjClose'}, inplace=True)
    return data

def transform_multi_data(data, symbol):
    ''' Changes column names into differentiable ones. '''
    for col in data.columns:
        data['{}_{}'.format(symbol, col)] = data[col]
        data = data.drop([col], axis=1)
    return data

def leave_basic(folder, data):
    if folder == 'tiingo':
        data = data.drop(['splitFactor', 'adjOpen', 'adjLow', 'adjHigh', 'divCash', 'adjVolume'], axis=1)
    return data

def get_pickle(folder, name, basic=True, resampler=False, as_is=False):
    df = read_pickle(join(STORAGE_PATH, folder, '{}.p'.format(name)))
    df.index = to_datetime(df.index)
    if not as_is:
        df = normalize(folder=folder, data=df)
        if basic:
            df = leave_basic(folder=folder, data=df)
        assert len(df.loc[df['Close'] == 0]) == 0, 'Data has zeros!'
        assert len(df.index[isinf(df).any(1)]) == 0, 'Data has inf!'
        assert len(df.index[isnan(df).any(1)]) == 0, 'Data has nan!'
        if not resampler:
            df = transform_multi_data(data=df, symbol=name)
    return df

def get_parquet(name):
    path = join(STORAGE_PATH, 'parq', '{}.parq'.format(name))
    pf = ParquetFile(path)
    return pf.to_pandas()

def join_data(folder, symbols, clr=False):
    ''' Makes one DataFrame for many symbols. '''
    with sw.timer('join_data'):
        init = get_pickle(folder=folder, name=symbols[0], basic=clr)
        for symbol in symbols[1:]:
            data = get_pickle(folder=folder, name=symbol)
            if data is not None:
                init = init.join(data, how='left')
        df = fill_forward(data=init)
    print(format_report(sw.get_last_aggregated_report()))
    return df

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
