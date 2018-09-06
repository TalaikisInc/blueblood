from os.path import join
from os import listdir

from clint.textui import colored
from pandas import concat, DataFrame
from numpy import dot, sqrt, random, sum

from app.data import get_pickle
from .vars import STORAGE_PATH
from .saves import save_weights
from app.stats import *
from .file_utils import filenames
from .date_utils import ensure_latest


def get_latest_allocs(name):
    tot = len([f for f in listdir(join(STORAGE_PATH, 'portfolios', 'weights')) if (name in f) & (f != '.gitkeep')]) - 1
    weights = get_pickle(join('portfolios', 'weights'), '{}_{}'.format(name, tot), as_is=True)
    del weights['Returns']
    del weights['Volatility']
    del weights['Ratio']
    return [weights.iloc[0].to_dict()]

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
    return df, adjdf, get_latest_allocs(name=name)

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

def portfolio_generator(df, adj_df, chunk_size, algo, com_df, symbols, name):
    num_assets = len(symbols)
    num_portfolios = 5000
    random.seed(101)

    for i in range(int(len(df.index)/chunk_size)):
        data = df.iloc[i*chunk_size:(i+1)*chunk_size]
        adj_future_data = adj_df.iloc[(i+1)*chunk_size:(i+2)*chunk_size]
        future_data = df.iloc[(i+1)*chunk_size:(i+2)*chunk_size]
        chunked_com = com_df.iloc[(i+1)*chunk_size:(i+2)*chunk_size]
        returns = data.copy()
        cov_daily = returns.cov()
        cov_annual = cov_daily * sqrt(252)

        port_returns = []
        port_volatility = []
        ratios = []
        stock_weights = []

        for portfolio in range(num_portfolios):
            weights = random.random(num_assets)
            weights /= sum(weights)
            returns_dot = dot(weights, returns.mean() * sqrt(252))
            volatility = sqrt(dot(weights.T, dot(cov_annual, weights)))
            returns_for_stats = (weights.T * returns).sum(axis=1)
            val = eval(algo[0])
            ratios.append(val)
            port_returns.append(returns_dot)
            port_volatility.append(volatility)
            stock_weights.append(weights)

        portfolio = { 'Returns': port_returns, 'Volatility': port_volatility,'Ratio': ratios }

        for counter, symbol in enumerate(symbols):
            portfolio[symbol] = [weight[counter] for weight in stock_weights]

        out = DataFrame(portfolio)
        column_order = ['Returns', 'Volatility', 'Ratio'] + ['{}'.format(stock) for stock in symbols]
        out = out[column_order]
        out.sort_values('Ratio', axis=0, ascending=False, inplace=True)
        save_weights(df=out, name='{}_{}'.format(name, i))
        portfolio_returns(data=future_data.copy(), adj_data=adj_future_data.copy(), symbols=symbols, name='{}_{}'.format(name, i), comms=chunked_com)

def get_current_weights(SELECTED_PORTFOLIOS, SELECTED_STRATEGIES):
    path = join('portfolios', 'tradeable')
    fs = filenames(path, resampled=True)
    fs += filenames(path, resampled=False)
    selected = SELECTED_PORTFOLIOS + SELECTED_STRATEGIES
    SELECTED_LST = [s['name'] for s in SELECTED_PORTFOLIOS] + [s['name'] for s in SELECTED_STRATEGIES]

    res = []
    total_weights = []
    for f in fs:
        name = f.split('.')[0]
        if name in SELECTED_LST:
            d = get_pickle(path, name, as_is=True)
            for s in selected:
                if s['name'] == name:
                    if s['type'] == 'cash':
                        arr = d * s['weight']
                    elif s['type'] == 'ports':
                        arr = d * s['weight'] / len([s['name'] for s in SELECTED_PORTFOLIOS if s['type'] == 'ports'])
                    elif s['type'] == 'strats':
                        arr = d * s['weight'] / len([s['name'] for s in SELECTED_STRATEGIES if s['type'] == 'strats'])
                    res.append(arr.T)
                    total_weights += list(arr.values[0])

    out = concat(res, axis=0)
    out.columns = ['W']
    out = out.groupby(out.index).sum()
    assert round(sum(total_weights), 2) == 1.0, 'Total index weights are not equal 100%!'
    print('% Weights')
    print(out)
    print('$ Weights')
    print(round(out * 100000, 2)) # Use defined capital if not via Trader API
    # @TODO count in shares

def latest_date_foreeach(symbols):
    for s in symbols:
        try:
            d = get_pickle('tiingo', s)
            ensure_latest(d, symbol=s)
        except Exception as err:
            print(colored.red('{}: {}'.format(s, err)))
