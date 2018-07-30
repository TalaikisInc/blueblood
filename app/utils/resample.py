from dask.dataframe.multi import concat
from clint.textui import colored
from pandas import concat
from numba import jit

from .methods import write_parq, read_parq
from .index import filenames
from app.data.local import to_pickle, get_pickle, normalize


def resample_dd(df, per):
    return df.resample(per)

def resample(df, name, folder='dukas', per='10T'):
    hl = (df['Ask'] + df['Bid']) / 2.0
    open = resample_dd(df=hl, per=per).first().compute()
    high = resample_dd(df=hl, per=per).max().compute()
    low = resample_dd(df=hl, per=per).min().compute()
    close = resample_dd(df=hl, per=per).last().compute()
    out = concat([open, high, low, close], axis=1, interleave_partitions=True)
    out.columns = ['Open', 'High', 'Low', 'Close']
    write_parq(df=out.dropna(), folder=folder, name='{}_{}'.format(name, per))

def resample_dukas_all(folder='dukas'):
    pers = ['1T', '5T', '15T', '30T', '60T', '240T', '1440T', '10800T', '43200T']
    symbols = [f.split('.')[0] for f in filenames(folder) if '.parq' in f]
    for s in symbols:
        df = read_parq(folder, s)
        for p in pers:
            resample(df=df, name=s, folder=folder, per=p)
            print(colored.green('Resampled {} {}'.format(s, p)))

@jit
def resample_df(folder, df, period):
    df = normalize(folder, df)
    open = df.Open.resample(period).last()
    high = df.High.resample(period).max()
    low = df.Low.resample(period).min()
    close = df.Close.resample(period).last()
    adj_close = df.Adjusted_close.resample(period).last()
    vol = df.Volume.resample(period).sum()
    return concat([open, high, low, close, adj_close, vol], axis=1)

def write_resampled_df(df, folder, s, p):
    to_pickle(data=df, folder=folder, name='{}_{}.p'.format(s, p))
    print(colored.green('Resampled {} {}'.format(s, p)))

def resample_all(folder='tiingo'):
    pers = ['1W', '1M']
    symbols = [f.split('.')[0] for f in filenames(folder) if (('.p' in f) & ('_' not in f))]
    for s in symbols:
        try:
            df = get_pickle(folder, s)
            for p in pers:
                df = resample_df(folder=folder, df=df, period=p)
                write_resampled_df(df=df, folder=folder, s=s, p=p)
        except Exception as err:
            print(colored.red(err))
