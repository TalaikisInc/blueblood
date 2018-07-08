from dask.distributed import Client, progress
import dask.dataframe as dd
from raccoon.dataframe import DataFrame
from panas import DataFrame as PandasDataFrame

client = Client(n_workers=2, threads_per_worker=2, memory_limit='1GB')


def read(path):
    return dd.read_parquet(path)

def rolling(df, window, method):
    return df.rolling(window=window).method()

def resample(df, period, method, compute=False):
    if compute:
        df.resample(period).method().compute()
    else:
        d.resample(period).method()
    return df

def loc(df, loc):
    return df.loc[loc].compute()

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

def sets(df):
    pass

def add():
    pass

def divide():
    pass

def multiply():
    pass

def get_cell():
    pass

def sort():
    pass

def iterrows():
    pass
