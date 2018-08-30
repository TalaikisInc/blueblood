from numpy import random, sum, dot, sqrt
from pandas import DataFrame
from matplotlib import pyplot as plt

from app.data import join_data


def min_variance(df):
    min_vol = df['Volatility'].min()
    max_sharpe = df['Sharpe Ratio'].max()

    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_vol]
    print('Min variance portfolio')
    print(min_variance_port.T)
    print('Max Sharpe portfolio')
    print(sharpe_portfolio.T)
    return(sharpe_portfolio, min_variance_port)

def generate_minvariance_portfolios(folder, symbols):
    '''
    Generates random min variance portfolios. Returns dataframe that
    can be plotted with app.plot.plot_portfolios
    '''

    assert type(symbols) == list, 'Symbols should be a list!'

    data = join_data(folder=folder, symbols=symbols, clr=True)
    data = data.dropna()
    returns_daily = data.pct_change()
    returns_annual = returns_daily.mean() * sqrt(252)
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * sqrt(252)

    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []

    num_assets = len(symbols)
    num_portfolios = 5000
    random.seed(101)

    for portfolio in range(num_portfolios):
        weights = random.random(num_assets)
        weights /= sum(weights)
        returns = dot(weights, returns_annual)
        volatility = sqrt(dot(weights.T, dot(cov_annual, weights)))
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)
        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    portfolio = {
        'Returns': port_returns,
        'Volatility': port_volatility,
        'Sharpe Ratio': sharpe_ratio
        }

    for counter, symbol in enumerate(symbols):
        portfolio[symbol+' Weight'] = [weight[counter] for weight in stock_weights]

    df = DataFrame(portfolio)

    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + ['{}_Weight'.format(stock) for stock in symbols]

    return df[column_order]

def main():
    df = generate_minvariance_portfolios()
    plot_portfolios(df=df)

def plot_portfolios(df):
    best = min_variance(df=df)
    df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio', cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    plt.scatter(x=best[0]['Volatility'], y=best[0]['Returns'], c='red', marker='D', s=200)
    plt.scatter(x=best[1]['Volatility'], y=best[1]['Returns'], c='blue', marker='D', s=200 )

    plt.xlabel('Volatility')
    plt.ylabel('E')
    plt.title('Efficient frontier')
    plt.show()
