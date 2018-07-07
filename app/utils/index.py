from os import listdir
from os.path import isfile, join, dirname

from clint.textui import colored
from pandas import DataFrame
from peewee import Field

from data.local import get_pickle, get_mt, META_PATH


def peewee_to_df(table):
    fields = [f for f in dir(table) if isinstance(getattr(table, f), Field)]
    data = list(table.select(*[getattr(table, fld) for fld in fields]).tuples())
    df = DataFrame.from_records(data, columns=table._meta.fields)

    if 'id' in fields:
        df.set_index('id', inplace=True)
    return df

def filenames(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def fill_forward(data):
    return data.fillna(method='ffill')

def clean(folder, data):
    if folder == 'fred':
        del data['realtime_start']
    if folder == 'mt':
        del data['Open']
        del data['High']
        del data['Low']
        del data['Volume']
    return data

def join_data(primary, folder, factors):
    i = 0
    for factor in factors:
        data = get_pickle(folder, factor)
        data = clean(folder=folder, data=data)
        data.columns = [factors[i]]
        primary = primary.join(data, how='left')
        i = i + 1
        return fill_forward(data=primary)

def convert_mt_pickle():
    BASE_DIR = dirname(dirname(__file__))
    fs = filenames(path=META_PATH)
    for f in fs:
        try:
            name = f.split('_')[3]
            per = f.split('_')[4].split('.')[0]
            dest_path = join(BASE_DIR, 'storage', 'mt', '{}_{}.p'.format(name, per))
            data = get_mt(name, per)
            if len(data) > 100:
                data.rename(columns={'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
                data.to_pickle(dest_path)
                print(colored.green('Converted for {} {}'.format(name, per)))
        except Exception as err:
            print(colored.red(err))

def periodize_returns(r, p=252):
    return ((1 + r) ^ p - 1)
