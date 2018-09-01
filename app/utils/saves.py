from os.path import join

from pandas import DataFrame

from .vars import STORAGE_PATH
from .date_utils import ensure_latest


def save_plot(plt, folder, name):
    plt.savefig(join(STORAGE_PATH, 'images', folder, '{}.png'.format(name)))
    plt.close()

def save_weights(df, name):
    df.to_pickle(join(STORAGE_PATH, 'portfolios', 'weights', '{}.p'.format(name)))

def save_strategy(df, name):
    #ensure_latest(df=df)
    df.to_pickle(join(STORAGE_PATH, 'strategies', '{}.p'.format(name)))

def save_indicator(df, name):
    #ensure_latest(df=df)
    df.to_pickle(join(STORAGE_PATH, 'indicators', '{}.p'.format(name)))

def save_port(data, name):
    ''' Helper for saving portfolios.'''
    ensure_latest(df=data)
    data.to_pickle(join(STORAGE_PATH, 'portfolios', '{}.p'.format(name)))

def save_tradeable(data, name):
    df = DataFrame([data[k] for k in data], data.keys())
    df.to_pickle(join(STORAGE_PATH, 'portfolios', 'tradeable', '{}.p'.format(name)))
