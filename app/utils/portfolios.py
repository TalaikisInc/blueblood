from os.path import join
from os import listdir

from pandas import concat

from app.data import get_pickle
from .vars import STORAGE_PATH


def get_latest_allocs(name, symbols):
    tot = len([f for f in listdir(join(STORAGE_PATH, 'portfolios', 'weights')) if (name in f) & (f != '.gitkeep')]) - 1
    weights = get_pickle(join('portfolios', 'weights'), '{}_{}'.format(name, tot), as_is=True)

    ws = []
    for i in range(len(weights.iloc[0].index)):
        for s in symbols:
            if s == weights.iloc[0].index[i]:
                ws.append(weights.iloc[0].values[i])
    return ws

def reconstruct_returns(name, symbols):
    fs = [f for f in listdir(join(STORAGE_PATH, 'portfolios', 'weights', 'returns')) if (name in f) & (f != '.gitkeep')]
    adjfs = [f for f in listdir(join(STORAGE_PATH, 'portfolios', 'weights', 'adj_returns')) if (name in f) & (f != '.gitkeep')]
    dfs = []
    adjdfs = []
    for f in fs:
        _name = f.split('.')[0]
        d = get_pickle(join('portfolios', 'weights', 'returns'), _name, as_is=True)
        dfs.append(d)
    for f in adjfs:
        _name = f.split('.')[0]
        d = get_pickle(join('portfolios', 'weights', 'adj_returns'), _name, as_is=True)
        adjdfs.append(d)
    df = concat(dfs, axis=1).sum(axis=1)
    adjdf = concat(adjdfs, axis=1).sum(axis=1)
    last_allocs = { 'sym': symbols, 'alloc': get_latest_allocs(name=name, symbols=symbols) }
    return df, adjdf, last_allocs

# @TODO:
def plot_portfolios(df):
    best_ratio = df.iloc[0]
    min_variance = df.loc[df['Volatility'] == df['Volatility'].min()]

    df.plot.scatter(x='Ratio', y='Returns', c='Volatility', cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=best_ratio['Ratio'], y=best_ratio['Returns'], c='red', marker='D', s=100)
    plt.scatter(x=min_variance['Ratio'], y=min_variance['Returns'], c='red', marker='D', s=100)

    plt.xlabel('Ratio')
    plt.ylabel('Returns')
    plt.title('Efficient frontier')
    plt.show()

def portfolio_returns(data, adj_data, symbols, name, comms, min_var=False):
    weights = get_pickle(join('portfolios', 'weights'), name, as_is=True)
    if min_var:
        best_ratio = weights.loc[weights['Volatility'] == weights['Volatility'].min()]
    best_ratio = weights.iloc[0]

    data['combined'] = 0
    adj_data['adj_combined'] = 0
    w = 0
    for s in symbols:
        w += best_ratio['{}'.format(s)]
        filtered_comms = comms[s].fillna(0.0) / len(comms[s].index) * 2
        data['comm'] = filtered_comms
        data['combined'] += best_ratio['{}'.format(s)] * data['{}_ret'.format(s)] - best_ratio['{}'.format(s)] * data['comm']
        adj_data['adj_combined'] += best_ratio['{}'.format(s)] * adj_data['{}_ret'.format(s)] - best_ratio['{}'.format(s)] * data['comm']

    assert round(w, 2) == 1.0, 'Allocations {}'.format(w)
    data['combined'].to_pickle(join(STORAGE_PATH, 'portfolios', 'weights', 'returns', '{}.p'.format(name)))
    adj_data['adj_combined'].to_pickle(join(STORAGE_PATH, 'portfolios', 'weights', 'adj_returns', '{}.p'.format(name)))
