from os import getenv

from requests import get
from pandas import DataFrame


URL = 'https://simfin.com/api/v1/'
KEY = getenv('SIMFIN_API')

def get_id(sym):
    url = '{}info/find-id/ticker/{}?api-key={}'.format(URL, sym, KEY)
    res = get(url)
    json = res.json()
    df = DataFrame(json)
    return int(df.iloc[0]['simId'])

def all_entries():
    url = '{}info/all-entities?api-key={}'.format(URL, KEY)

def get_company(id):
    url = '{}companies/id/{}?api-key={}'.format(URL, id, KEY)

def get_statements(id):
    url = '{}companies/id/{}/statements/standardised?api-key={}'.format(URL, id, KEY)
    res = get(url)
    json = res.json()
    df = DataFrame(json)
    print(df)

def get_statement_named(sym):
    id = get_id(sym=sym)
    get_statements(id=id)

def shares_outstanding(id):
    url = '{}companies/id/{}/shares/aggregated?api-key={}'.format(URL, id, KEY)
