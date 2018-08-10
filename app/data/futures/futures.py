from urllib.request import urlretrieve
from os import listdir
from os.path import dirname, join, exists
from datetime import datetime

from pandas import DataFrame, read_csv
from numpy import  nan

from app.utils import STORAGE_PATH


m_codes = ['F','G','H','J','K','M','N','Q','U','V','X','Z']
codes = dict(list(zip(m_codes,list(range(1,len(m_codes)+1)))))
SYMBOL = 'VX'
DIR = join(STORAGE_PATH, 'futures', SYMBOL)

def save_data(year, month, path, forceDownload=False):
    ''' Get future from CBOE and save to file '''
    fName = 'CFE_{0}{1}_{2}.csv'.format(m_codes[month], str(year)[-2:], SYMBOL)
    if exists(join(DIR, fName)) or forceDownload:
        print('File already downloaded, skipping')
        return
    
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
            df = read_csv(join(dataDir, fName))

            code = fName.split('.')[0].split('_')[1]
            month = '%02d' % codes[code[0]]
            year = '20'+code[1:]
            newCode = year + '_' + month
            data[newCode] = df
        except Exception as e:
            print('Could not process:', e)
        
        
    full = DataFrame()
    for k, df in data.items():
        s = df['Settle']
        s.name = k
        s[s<5] = nan
        if len(s.dropna())>0:
            full = full.join(s,how='outer')
        else:
            print(s.name, ': Empty dataset.')
    
    full[full<5] = nan
    full = full[sorted(full.columns)]
        
    # use only data after this date
    #startDate = datetime(2008,1,1)
    
    idx = full.index #>= startDate
    full = full.ix[idx,:]
    
    fName = join(dataDir, 'output', '{}.csv'.format(SYMBOL))
    print('Saving to ', fName)
    full.to_csv(fName)


def download_futures():
    '''
    for year in range(2005, 2018):
        for month in range(12):
            print('Getting data for {0}/{1}'.format(year, month + 1))
            save_data(year, month, DIR)

    print('Raw wata was saved to {0}'.format(DIR))
    '''
    
    build_table(DIR)
