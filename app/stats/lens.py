from os.path import join

from .alphalens.tears import create_full_tear_sheet, create_event_study_tear_sheet
from .alphalens.utils import get_clean_factor_and_forward_returns
from app.data import get_pickle, transform_multi_data, join_data
from app.models.alpha import all_alphas, alpha
from app.utils import makedir, DATA_SOURCE, filenames
from .functions import clean_prices, clean_alpha, transform_for_analysis


def run_factor_analysis(factor, prices, f):
    factor_data = get_clean_factor_and_forward_returns(factor, prices, quantiles=5)
    create_full_tear_sheet(factor_data=factor_data, f=f)

def run_event_analsyis(event, prices):
    factor_data = get_clean_factor_and_forward_returns(event, prices, quantiles=None, bins=1,
        periods=(1, 2, 3, 4, 5, 10, 15), filter_zscore=None)
    create_full_tear_sheet(factor_data)
    return factor_data

def event_distribution(event, prices):
    create_event_study_tear_sheet(run_event_analsyis(event=event, prices=prices), prices, avgretplot=(5, 10))

def run_factor(data, model, BASKET):
    df = alpha(model=int(model), symbols=BASKET, train=True)
    df = clean_alpha(data=df, symbols=BASKET, d_type='eod')
    df = transform_for_analysis(df)
    makedir(join('images', 'factors', str(model)))
    run_factor_analysis(factor=df, prices=data.dropna(), f=model)

def run_analyze(model):
    try:
        model = int(model)
    except:
        model = None
        pass
    '''
    BASKET = ['BSX', 'AIG', 'INTU', 'INTC', 'HON', 'DUK', 'NTAP', 'COL', 'ABT', 'ADSK', 'NUE',
        'MU', 'TIF', 'ADBE', 'FDX', 'NKE', 'TAP', 'SCHW', 'STI', 'CIT', 'LNC', 'MAT', 'ARNC',
        'ADI', 'AFL', 'KEY', 'HD', 'OKE', 'LOW', 'RF', 'OI', 'AES', 'LUV', 'TXT', 'UNH', 'DVN',
        'CCL', 'MRO', 'EOG', 'T', 'AVY', 'CI', 'BK', 'CSR', 'AAPL', 'ZBH', 'CTXS', 'ALL', 'SHW',
        'COF', 'SNA', 'AET', 'SYY', 'UNM', 'GTE', 'GWW', 'BVSN', 'BLL', 'COST', 'CS', 'HPQ',
        'CTAS', 'AMAT', 'WFC', 'EFU', 'HRB', 'ADM', 'NWL', 'EFX', 'PGR', 'BBT', 'NVDA', 'ARC',
        'SGI', 'JPM', 'GIS', 'PHM', 'PCAR', 'PKI', 'NOC', 'SUB', 'APD', 'ITW', 'OXY', 'FMC',
        'BDX', 'AXP', 'SLB', 'TX', 'TWX', 'AGN', 'ZION', 'CMA', 'A', 'TKR', 'FISV', 'CCK',
        'AEE', 'APA', 'TJX', 'CSCO', 'GRA', 'AMGN', 'DOV', 'WMT', 'EQR', 'LMT', 'BAC', 'NC',
        'PH', 'VMC', 'VO', 'EMR', 'HAS', 'ECL', 'CINF', 'C', 'DNB', 'AGC', 'BGG', 'TMK', 'SWK',
        'BFO', 'APC', 'LLY', 'NEM', 'NEE', 'VZ', 'PBY', 'SMI', 'PNC', 'MSFT', 'H', 'CMS',
        'BAX', 'ADP', 'CAH', 'SYK', 'EMN', 'PCH', 'ABC', 'KSU', 'IFF', 'CA', 'CLX', 'TGT',
        'JNJ', 'SRV', 'AON', 'VFC', 'MMC', 'FLR', 'ORCL', 'BBY', 'CBS', 'MAS', 'CAG', 'RAD',
        'GPC', 'HES', 'RHI', 'AZO', 'CNP', 'CTL', 'XLNX', 'MCD', 'LB', 'CSX', 'YUM', 'USB',
        'GPS', 'PX', 'CHA', 'MDT', 'WMB', 'JWN', 'CMI', 'IPG', 'DIS']
    '''
    BASKET = ['QQQ', 'SPY', 'IWM', 'EEM', 'TLT']

    initial = get_pickle(DATA_SOURCE, BASKET[0])
    initial = transform_multi_data(data=initial, symbol=BASKET[0])
    data = join_data(primary=initial, folder=DATA_SOURCE, symbols=BASKET[1:])
    data = clean_prices(data=data, symbols=BASKET, d_type='eod')

    if model is None:
        for i in all_alphas():
            print('Alpha %s' % i)
            run_factor(data, i, BASKET)
    else:
        run_factor(data, model, BASKET)
