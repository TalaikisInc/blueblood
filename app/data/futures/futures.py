from urllib.request import urlretrieve
from os import listdir
from os.path import dirname, join, exists
from datetime import datetime, timedelta

from clint.textui import colored
from pandas import DataFrame, read_csv
from pandas.tseries.offsets import Week
from numpy import  nan

from app.utils.vars import STORAGE_PATH


m_codes = ['F','G','H','J','K','M','N','Q','U','V','X','Z']
codes = dict(list(zip(m_codes,list(range(1,len(m_codes)+1)))))
SYMBOL = 'VX'
DIR = join(STORAGE_PATH, 'futures', SYMBOL)

def vx_expiry(year, month):
    # @TODO add holidays and should be month here:
    # # https://markets.cboe.com/us/futures/market_statistics/historical_data/
    t = datetime(year, month, 1) + timedelta(days=30)
    offset = Week(weekday=4)
    if t.weekday() != 4:
        t_new = t + 3 * offset
    else:
        t_new = t + 2 * offset
    t_exp = t_new - timedelta(days=30)
    return t_exp

def save_data(year, month, path, forceDownload=False):
    ''' Get future from CBOE and save to file '''
    fName = 'CFE_{0}{1}_{2}.csv'.format(m_codes[month], str(year)[-2:], SYMBOL)
    if not forceDownload:
        if exists(join(DIR, fName)):
            print('File already downloaded, skipping')
            return

    if (year >= 2018) & (month >= 2):
        e = vx_expiry(year, month)
        urlStr = 'https://markets.cboe.com/us/futures/market_statistics/historical_data/products/csv/VX/{}'.format(e)
    else:
        urlStr = 'http://cfe.cboe.com/Publish/ScheduledTask/MktData/datahouse/{0}'.format(fName)
    print('Getting: %s' % urlStr)
    try:
        urlretrieve(urlStr, path+'\\'+fName)
    except Exception as e:
        print(e)

def build_table(dataDir):
    ''' Create single data sheet '''
    files = listdir(dataDir)

    data = {}
    for fName in files:
        print('Processing: ', fName)
        try:
            cols = ['Futures', 'Open', 'High', 'Low', 'Close', 'Settle', 'Change', 'Total Volume', 'EFP', 'Open Interest']
            df = read_csv(join(dataDir, fName), skiprows=2, names=cols, parse_dates=True)
            code = fName.split('.')[0].split('_')[1]
            month = '%02d' % codes[code[0]]
            year = '20'+code[1:]
            newCode = year + '_' + month
            data[newCode] = df
        except Exception as e:
            print(colored.red('Could not process:', e))
            continue
        
        
    full = DataFrame()
    for k, df in data.items():
        s = df['Settle'].copy()
        s.name = k
        s[s<5] = nan
        if len(s.dropna())>0:
            full = full.join(s,how='outer')
        else:
            print(colored.red(s.name, ': Empty dataset.'))
    
    full[full<5] = nan
    full = full[sorted(full.columns)]
    
    idx = full.index #>= startDate
    full = full.ix[idx,:]
    
    fName = join(dataDir, 'output', '{}.csv'.format(SYMBOL))
    print(colored.green('Saving %s' % fName))
    full.to_csv(fName)

def download_futures(last=False, forceDownload=False):
    ty = datetime.now().year + 1
    if last:
        r = range(ty-1, ty)
    else:
        r = range(2005, ty)
    print(r)

    for year in r:
        for month in range(12):
            try:
                print('Getting data for {0}/{1}'.format(year, month + 1))
                save_data(year, month, DIR, forceDownload=forceDownload)
            except Exception as err:
                print(colored.red(err))

    print('Raw wata was saved to {0}'.format(DIR))
    
    build_table(DIR)
