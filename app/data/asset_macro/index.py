from os import getenv
from http.client import HTTPConnection

from pandas import DataFrame


class AssetMacro(object):
    user_name = None
    password = None
    conn = None
    headers = None
    payload = None

    def __init__(self, user_name, password):
        self.auth(user_name, password)
        self.conn = HTTPConnection('api.assetmacro.com')

    def auth(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.headers = {'Authorization': '{};{}'.format(self.user_name, self.password)}

    def get_vars(self):
        self.conn.request(method='GET', url='/vars', headers=self.headers)
        response = self.conn.getresponse()
        data = response.read()
        str_data = data.decode('utf-8')
        return str_data.split(',')

    def load_data(self, var_name, start_date=None, end_date=None):
        v = self.get_vars()
        if var_name not in v:
            raise ValueError('Variable name not found, check the get_vars() result.')
        params = 'name={}'.format(quote(var_name))
        if start_date:
            params += '&start_date={}'.format(start_date)
        if end_date:
            params += '&end_date={}'.format(end_date)
        url = "/query?" + params
        self.conn.request(method="GET", url=url, headers=self.headers)
        response = self.conn.getresponse()
        if response.status == 200:
            data = response.read()
            str_data = data.decode("utf-8") 
            data_rows = str_data.split('\r\n')
            if len(data_rows) <= 1:
                return data_rows
            data_arr = []
            for d in data_rows:
                data_arr.append(d.split(','))
            d = data_arr[:-1] # skip the last empty row
            return DataFrame(d[1:], columns=d[0])
        else:
            raise ValueError('Server error {} {}'.format(response.status, response.reason))
            return None

def get_am_vars():
    am = AssetMacro(getenv('ASSET_MACRO_USER'), getenv('ASSET_MACRO_PASS'))
    v = am.get_vars()
    print(v)

def get_am_data():
    am = AssetMacro(getenv('ASSET_MACRO_USER'), getenv('ASSET_MACRO_PASS'))
    d = am.load_data('7468', '2014-01-01', '2017-12-31')
    print (d)
