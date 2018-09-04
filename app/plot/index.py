from os.path import dirname, join
from collections import Counter
from datetime import timedelta

from matplotlib import pyplot as plt, cm
from mpl_finance import candlestick_ohlc
from numpy import array, sort, unique, linspace, nan, where
from statsmodels.api import qqplot
from scipy.stats import t
from sklearn.manifold import TSNE
from seaborn import heatmap, despine
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette(sns.color_palette('RdBu', n_colors=5))
BLUE1, = sns.color_palette('muted', 1)
from pandas import date_range

from app.stats import percentiles, drawdowns, returns_by_day, returns_by_year, rolling_sharpe
from app.utils import save_plot
from app.data import get_pickle


def drawdown(cumulative, folder, save=False):
    dd = drawdowns(cumulative=cumulative)
    plt.plot(dd, label='Drawdown', lw=3)
    plt.xlabel('Time, t')
    plt.ylabel('Value')
    plt.legend()
    if save:
        save_plot(plt=plt, folder=folder, name='drawdowns.png')
    else:
        plt.show()

def drawdown_to_percentile(cumulative, folder, save=False):
    d = drawdowns(cumulative=cumulative).dropna()
    dd = d.loc[d != 0]
    if len(dd) > 100:
        x = percentiles(dd)
        y = array([i for i in range(100)])
        plt.plot(x, y/100)
        plt.xlabel('Drawdown')
        plt.ylabel('Probability')
        if save:
            save_plot(plt=plt, folder=folder, name='drawdown_percentile.png')
        else:
            plt.show()

def qq(res):
    fig = qqplot(res, stats.t, fit=True, line='45')
    plt.show()

def hist(data, other):
    _sorted = sort(data)
    plt.hist(_sorted, bins=100)
    if other:
        _sorted = sort(other)
        plt.hist(_sorted, bins=100)
    plt.show()

def tsne(X, y):
    model = TSNE(n_components=2, random_state=0)
    x_2d = model.fit_transform(X)
    markers=('s', 'd', 'o', '^', 'v')
    color_map = {0: 'red', 1: 'blue', 2: 'lightgreen', 3: 'purple', 4: 'cyan'}
    plt.figure()
    for idx, cl in enumerate(unique(y_test)):
        plt.scatter(x=x_2d[y==cl, 0], y=x_2d[y==cl, 1], c=color_map[idx], marker=markers[idx], label=cl)
    plt.xlabel('X in t-SNE')
    plt.ylabel('Y in t-SNE')
    plt.legend(loc='upper left')
    plt.title('t-SNE visualization of test data')
    plt.show()

def plot_hdbscan(X, labels,  n_clusters):
    unique_labels = set(labels)
    colors = plt.cm.Spectral(linspace(0, 1, len(unique_labels)))
    fig = plt.figure(figsize=plt.figaspect(1))
    hdb_axis = fig.add_subplot('121')

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        hdb_axis.plot(X[labels == k, 0], X[labels == k, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=3)

    hdb_axis.set_title('Estimated number of clusters: %d' % n_clusters)
    plt.show()

def corr_heatmap(returns, name, save=False):
    ''' Helper for correlation heatmap.'''
    ax = heatmap(returns.corr())
    name = name[0].upper() + name[1:].lower()
    title = '{} Heatmap'.format(name)
    plt.title(title)
    if save:
        save_plot(plt=plt, folder='index', name=name)
    else:
        plt.show()

def hdns_barplot(hdbs):
    label_counts = Counter(hdbs.labels_)
    xs, ys = [], []
    for k, v in label_counts.items():
        xs.append(k)
        ys.append(v)

    plt.bar(xs, ys)
    plt.xticks(range(-1, len(label_counts)))
    plt.ylabel('Counts')
    plt.xlabel('Cluster label')
    plt.title('Sizes ({} clusters found by hdbscan)'.format(len(label_counts) - 1))
    plt.show()
 
def candles(data, symbol):
    data = data.loc[:, ['{}_Open'.format(symbol), '{}_High'.format(symbol), '{}_Low'.format(symbol), '{}_Close'.format(symbol)]]

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, zip(data.index.tolist(), (data['{}_Open'.format(symbol)].tolist(), data['{}_High'.format(symbol)].tolist(),
        data['{}_Low'.format(symbol)].tolist(), data['{}_Close'.format(symbol)].tolist())), colorup='green', colordown='red', width=.4)
    plt.show()

def compare(val, title, lim=None):
    df = get_pickle('tiingo', 'SPY')
    market = df['SPY_AdjClose'].pct_change().cumsum()
    if lim is not None:
        market = market.loc[lim:]

    fig = plt.figure(figsize=(16,10))
    ax1 = fig.add_subplot(111)
    ax1.plot(val, color=BLUE1)
    ax1.set_ylabel('Indicator')

    ax2 = ax1.twinx()
    ax2.plot(market, 'r-')
    ax2.set_ylabel('S&P500', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.title(title)
    return plt

def hline(signal, values, per):
    index = [i for i in signal.index]

    end_idx = where(signal != 0, index, nan)
    for e in end_idx:
        if type(e) != float:
            x = date_range(end=e, periods=per)
            val = values.loc[e]
            y = [val] * per
            plt.plot(x, y, color='r')

    return plt

def save_yearly_returns(returns, folder):
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    despine()
    ax.yaxis.grid(linestyle=':')
    returns.plot(kind='bar')
    ax.set_title('Yearly Returns, %', fontweight='bold')
    ax.set_ylabel('%')
    ax.set_xlabel('Year')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.xaxis.grid(False)
    save_plot(plt=plt, folder=folder, name='yearly_returns')

def cumulate_returns(x):
    return x.cumsum()[-1]

def monthly_heatmap(returns, folder):
    returns = returns.groupby([lambda x: x.year, lambda x: x.month]).apply(cumulate_returns)
    returns = returns.to_frame().unstack()
    returns = round(returns, 3)
    returns.rename(columns={ 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
        inplace=True)
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    heatmap(returns, annot=True, fmt='0.2f', annot_kws={'size': 8}, alpha=1.0, center=0.0, cbar=False, cmap=cm.RdYlGn, ax=ax)
    ax.set_title('Monthly Returns, %', fontweight='bold')
    save_plot(plt=plt, folder=folder, name='monthly_returns')

def rolling_yearly_returns(returns, folder):
    yr = returns.rolling(window=252).mean()
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    yr.plot()
    ax.axhline(0.0)
    ax.set_title('Rolling Yearly Returns, %', fontweight='bold')
    save_plot(plt=plt, folder=folder, name='rolling_yearly_returns')

def rolling_sharpe_plot(returns, folder):
    rs = rolling_sharpe(returns=returns, rf=0.0, per=63)
    plt.figure(figsize=(12,8))
    ax = plt.gca()
    rs.plot()
    ax.axhline(0.0)
    ax.set_title('Rolling Yearly Returns, %', fontweight='bold')
    save_plot(plt=plt, folder=folder, name='rolling_yearly_returns')

def plot_returns(returns, folder):
    d = returns_by_day(returns=returns)
    y = returns_by_year(returns=returns)
    save_yearly_returns(returns=y, folder=folder)
    monthly_heatmap(returns=d, folder=folder)
    rolling_yearly_returns(returns=d, folder=folder)
    drawdown(cumulative=d.cumsum(), folder=folder, save=True)
    rolling_sharpe_plot(returns=d, folder=folder)
    drawdown_to_percentile(cumulative=d.cumsum(), folder=folder, save=True)
