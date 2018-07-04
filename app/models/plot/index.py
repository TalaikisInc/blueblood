from os.path import dirname, join

from numpy import maximum
from matplotlib import pyplot as plt


BASE_PATH = join(dirname(dirname(dirname(__file__))), "storage", "plots")

def plot(data, title, save=False):
    plt.style.use(['bmh'])
    fig, ax = plt.subplots(1)
    fig.suptitle(title, fontsize=16)
    ax.set_xlabel('Time, t')
    ax.set_ylabel(title)
    plt.plot(data[0], data[1])
    if save:
        path = join(BASE_PATH, "{}.png".format(title))
        plt.savefig(path)
    else:
        plt.show()


def drawdown(cumulatives, title, save=False):
    max = maximum.accumulate(cumulatives.dropna())
    dd = cumulatives - max

    plt.plot(dd, label="Drawdown", lw=3)
    plt.xlabel("Time, t")
    plt.ylabel("Value")
    plt.legend()
    if save:
        path = join(BASE_PATH, "{}.png".format(title))
        plt.savefig(path)
    else:
        plt.show()
