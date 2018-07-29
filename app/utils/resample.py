from dask.dataframe.multi import concat
from numpy import sum
from clint.textui import colored

from .methods import write_parq, read_parq
from .index import filenames
from app.data import to_pickle, get_pickle


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

def resample_df(df, period, method, compute=False):
    if compute:
        df.resample(period)[method].compute()
    else:
        df.resample(period)[method]
    return df

def resample_all(folder='tiingo'):
    pers = ['5B', '1W', '1M']
    symbols = [f.split('.')[0] for f in filenames(folder) if '.p' in f]
    for s in symbols:
        df = get_pickle(folder, s)
        for p in pers:
            to_pickle(resample_df(df=df, period=p, method=sum()), folder, '{}_{}.p'.format(s, p))
            print(colored.green('Resampled {} {}'.format(s, p)))
