from os import getenv
from datetime import datetime

from clint.textui import colored
from requests import get
from pandas import DataFrame, concat

from app.data import to_pickle
from app.variables import SELECTED_FUNDAMENTALS


URL = 'https://simfin.com/api/v1/'
KEY = getenv('SIMFIN_API')

def get_id(sym):
    try:
        url = '{}info/find-id/ticker/{}?api-key={}'.format(URL, sym, KEY)
        res = get(url)
        json = res.json()
        df = DataFrame(json)
        return int(df.iloc[0]['simId'])
    except Exception as err:
        print(colored.red(err))

def all_entries():
    url = '{}info/all-entities?api-key={}'.format(URL, KEY)

def get_company(id):
    url = '{}companies/id/{}?api-key={}'.format(URL, id, KEY)

def construct_name(sym, stype, ptype, fyear):
    if stype == 'pl':
        stype = 'profit_loss'
    elif stype == 'bs':
        stype = 'balance_sheet'
    elif stype == 'cf':
        stype = 'vash_flow'
    return '{}_{}_{}_{}'.format(sym, fyear, ptype, stype)

def get_statements(id, stype, ptype, fyear):
    try:
        url = '{}companies/id/{}/statements/standardised?stype={}&ptype={}&fyear={}&api-key={}'.format(URL, id, stype, ptype, fyear, KEY)
        res = get(url)
        json = res.json()
        return DataFrame(json['values'])
    except Exception as err:
        print(colored.red(err))

def get_all_statements(sym):
    stypes = ['pl', 'bs', 'cf']
    ptypes = ['Q1', 'Q2', 'Q3', 'Q4', 'TTM', 'FY']
    years = range(2007, datetime.now().year)

    id = get_id(sym=sym)
    if id is not None:
        for stype in stypes:
            print(stype)
            try:
                for year in years:
                    print(year)
                    for ptype in ptypes:
                        print(ptype)
                        df = get_statements(id=id, stype=stype, ptype=ptype, fyear=year)
                        if df is not None:
                            name = construct_name(sym=sym, stype=stype, ptype=ptype, fyear=year)
                            to_pickle(df, 'fundamentals', name)
                            print(colored.green('Saved %s' % name))
            except Exception as err:
                print(colored.red(err))

def process_fundamentals():
    for sym in SELECTED_FUNDAMENTALS:
        get_all_statements(sym=sym)

def shares_outstanding(id):
    url = '{}companies/id/{}/shares/aggregated?api-key={}'.format(URL, id, KEY)
