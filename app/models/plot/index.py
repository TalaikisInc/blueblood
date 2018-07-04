from os.path import dirname, join

from matplotlib import pyplot as plt


def plot(data, title, save=False):
    plt.style.use(['bmh'])
    fig, ax = plt.subplots(1)
    fig.suptitle(title, fontsize=16)
    ax.set_xlabel('Time, t')
    ax.set_ylabel(title)
    plt.plot(data[0], data[1])
    if save:
        BASE_PATH = join(dirname(dirname(dirname(__file__))), "storage", "plots")
        path = join(BASE_PATH, "{}.png".format(title))
        plt.savefig(path)
    else:
        plt.show()
