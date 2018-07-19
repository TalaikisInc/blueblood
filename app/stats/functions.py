from pandas import DataFrame, MultiIndex
from clint.textui import colored


def symbol_remover(data, symbols):
    for s in symbols:
        if len(data[s].dropna()) == 0:
            del data[s]
            print(colored.red('Removed {}'.format(s)))
    print(colored.red('Remove those from the basket too.'))
    return data

def clean_alpha(data, symbols, d_type):
    if d_type == 'accepted':
        for s in symbols:
            data = data.drop([
                '{}_Open'.format(s),
                '{}_High'.format(s),
                '{}_Low'.format(s),
                '{}_Close'.format(s),
                '{}_Volume'.format(s),
                '{}_Div'.format(s),
                '{}_Split'.format(s),
                '{}_Diff'.format(s),
                '{}_AdjClose'.format(s)
            ], axis=1)
    else:
        for s in symbols:
            data = data.drop([
                '{}_Open'.format(s),
                '{}_High'.format(s),
                '{}_Low'.format(s),
                '{}_Close'.format(s),
                '{}_Volume'.format(s),
                '{}_Diff'.format(s),
                '{}_Adjusted_close'.format(s)
            ], axis=1)
    if len(data.dropna()) == 0:
        print(colored.red('Some symbols have no data, going to delete them'))
        data = symbol_remover(data=data, symbols=symbols)
    return data

def clean_prices(data, symbols, d_type):
    if d_type == 'accepted':
        for s in symbols:
            data = data.drop([
                '{}_Open'.format(s),
                '{}_High'.format(s),
                '{}_Low'.format(s),
                '{}_Volume'.format(s),
                '{}_Div'.format(s),
                '{}_Split'.format(s),
                '{}_AdjClose'.format(s)
            ], axis=1)
            data.rename(columns={ '{}_Close'.format(s): s}, inplace=True)
    else:
        for s in symbols:
            data = data.drop([
                '{}_Open'.format(s),
                '{}_High'.format(s),
                '{}_Low'.format(s),
                '{}_Volume'.format(s),
                '{}_Adjusted_close'.format(s)
            ], axis=1)
            data.rename(columns={'{}_Close'.format(s): s}, inplace=True)
    return data

def transform_for_analysis(data):
    return DataFrame(data.dropna().stack(), index=MultiIndex.from_product([data.index, data.columns], names=['date', 'symbol']))
