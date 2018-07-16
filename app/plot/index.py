from os.path import dirname, join

from matplotlib import pyplot as plt
from numpy import array, sort
from statsmodels.api import qqplot
from scipy.sttats import t

from stats import percentiles, drawdowns
BASE_PATH = join(dirname(dirname(dirname(__file__))), 'storage', 'plots')


def plot(data, title, comparison=[], save=False):
    plt.style.use(['bmh'])
    fig, ax = plt.subplots(1)
    fig.suptitle(title, fontsize=16)
    ax.set_xlabel('Time, t')
    ax.set_ylabel(title)
    ax.plot(data, lw=2, color='b')
    if len(comparison) > 0:
        for p in comparison:
            ax.plot(p)
    if save:
        path = join(BASE_PATH, '{}.png'.format(title))
        plt.savefig(path)
    else:
        plt.show()

def drawdown(cumulative, title, save=False):
    dd = drawdowns(cumulative=cumulative)
    plt.plot(dd, label='Drawdown', lw=3)
    plt.xlabel('Time, t')
    plt.ylabel('Value')
    plt.legend()
    if save:
        path = join(BASE_PATH, '{}.png'.format(title))
        plt.savefig(path)
    else:
        plt.show()

def drawdown_to_percentile(cumulative, title, save=False):
    d = drawdowns(cumulative=cumulative).dropna()
    dd = d.loc[d != 0]
    if len(dd) > 100:
        x = percentiles(dd)
        y = array([i for i in range(100)])
        plt.plot(x, y/100)
        plt.xlabel('Drawdown')
        plt.ylabel('Probability')
        if save:
            path = join(BASE_PATH, '{}.png'.format(title))
            plt.savefig(path)
        else:
            plt.show()

def qq(res):
    fig = qqplot(res, stats.t, fit=True, line='45')
    plt.show()

def hist(data):
    sorted = sort(data)
    plt.hist(sorted, bins=100)
    plt.show()
