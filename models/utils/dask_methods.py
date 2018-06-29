from dask.distributed import Client, progress
import dask.dataframe as dd

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

def sets(df):
    pass
