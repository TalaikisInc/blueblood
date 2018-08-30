from os.path import join

from backtrader import WriterFile

from app.utils import STORAGE_PATH


def write(cerebro, symbol, c):
    cerebro.addwriter(WriterFile, close_out=True, csv=True, out=join(STORAGE_PATH, 'outputs', 'tests', 'bt', 'bt_{}_{}.csv'.format(symbol, c)), rounding=2)
    return cerebro
    
def plot(cerebro, symbol, c, show=False):
    if show:
        cerebro.plot(style='bar', volume=False, show=True)
    cerebro.plot(style='bar', volume=False, path=join(STORAGE_PATH, 'outputs', 'tests', 'bt', 'bt_{}_{}.png'.format(symbol, c)))
