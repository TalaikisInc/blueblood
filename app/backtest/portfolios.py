from pandas import concat
from matplotlib import pyplot as plt

from app.variables import PORTFOLIOS
from app.data.local import get_pickle, normalize


def see_portfolios():
    data = get_pickle('tiingo', 'SPY')
    data = normalize('tiingo', data)
    bench = data['Adjusted_close'].pct_change()

    ports = []
    names = []
    for p in PORTFOLIOS:
        total_alloc = 0
        print(p.name)
        data['Adjusted_close'] = 0
        data = data['Adjusted_close']
        for s in p.alloc:
            tmp = get_pickle('tiingo', s[0])
            tmp = normalize('tiingo', tmp)
            data += tmp['Adjusted_close'].pct_change() * s[1]
            total_alloc += s[1]
        ports.append(data)
        names.append(p.name)
        print(total_alloc)

    df = concat(ports + [bench], axis=1).dropna()
    df.columns = names + ['Benchmark']
    df.cumsum().plot()
    plt.show()
