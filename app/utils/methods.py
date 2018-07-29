from os.path import join

# from dask.distributed import Client, progress
from dask.dataframe import read_parquet, read_csv, to_parquet, from_pandas
from raccoon.dataframe import DataFrame
from pandas import DataFrame as PandasDataFrame

# client = Client(n_workers=2, threads_per_worker=2, memory_limit='1GB')
from .index import STORAGE_PATH


def read_parq(folder, name):
    return read_parquet(join(STORAGE_PATH, folder, '{}.parq'.format(name)))

def write_parq(df, folder, name, pd=False):
    if pd:
        to_parquet(from_pandas(df), join(STORAGE_PATH, folder, '{}.parq'.format(name)))
    else:
        to_parquet(df, join(STORAGE_PATH, folder, '{}.parq'.format(name)))

def parq_to_csv(folder, name):
    df = read_parq(folder=folder, name=name)
    df.compute().to_csv(join(STORAGE_PATH, folder, '{}.csv'.format(name)))

def read(folder, name):
    if folder == 'dukas':
        data = read_csv(join(STORAGE_PATH, folder, '{}.csv'.format(name)), parse_dates=[0])
        data.columns = ['Time', 'Ask', 'Bid', 'Ask_volume', 'Bid_volume']
        data = data.set_index('Time')
    return data

def rolling(df, window, method):
    return df.rolling(window=window).method()

def apply(df, method):
    return df.apply(method, meta=object).compute()

def train(partition, method):
    estimator = method()
    estimator.fit(partition[['x']].values, partition.y.values)
    return estimator

def rc_to_pd(raccoon_df):
    data = raccoon_df.to_dict(index=False)
    return PandasDataFrame(data, columns=raccoon_df.columns, index=raccoon_df.index)

def pd_to_rc(df):
    columns = df.columns.tolist()
    data = dict()
    pandas_data = df.values.T.tolist()
    for i in range(len(columns)):
        data[columns[i]] = pandas_data[i]
    index = df.index.tolist()
    index_name = df.index.name
    index_name = 'index' if not index_name else index_name
    return DataFrame(data=data, columns=columns, index=index, index_name=index_name)
