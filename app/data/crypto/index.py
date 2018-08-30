from os.path import join
from datetime import datetime

import ccxt
from clint.textui import colored
from peewee import IntegrityError
from pandas import DataFrame
from requests.exceptions import HTTPError
from numpy import array

from app.db import DB, CryptoExchange, CryptoMarket
from app.variables import EXCHANGES
from app.data import to_pickle, get_pickle
from app.utils.file_utils import filenames


def put_exchanges():
    for e in ccxt.exchaanges:
        print(e)
        try:
            if e is not None:
                CryptoExchange.create(title=e)
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(colored.red(err))

def insert_market(exchange, name):
    for market in  exchange.load_markets():
        print(market)
        try:
            CryptoMarket.create(market=market, exchange=CryptoExchange.get(title=name).id)
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(colored.red(err))

def get_exchanges():
    return [e.title for e in CryptoExchange.select()]

def get_markets(exchange):
    id = CryptoExchange.get(CryptoExchange.title == exchange)
    markets = CryptoMarket.select().where(CryptoMarket.exchange == id.id)
    return [m.market for m in markets]

def put_markets():
    for exchange in EXCHANGES:
        print(colored.green(exchange[0]))
        insert_market(exchange=exchange[1], name=exchange[0])

def get_quotes():
    for exchange in EXCHANGES:
        for instrument in get_markets(exchange=exchange[0]):
            try:
                print(instrument)
                return exchange[1].fetch_ticker(instrument)
            except Exception as err:
                print(colored.red(err))

def get_balance(exchange):
    return exchange.fetch_balance()

def get_crypto_balances():
    return DataFrame([exchange[1].fetch_balance() for exchange in EXCHANGES])

def get_account_info():
    return DataFrame([exchange[1].private_post_account_infos() for exchange in EXCHANGES])

def get_order_book(exchange, sym='BTC/USDT'):
    return DataFrame(exchange.fetch_order_book(sym))

def get_order_books(sym='BTC/USDT'):
    return DataFrame([exchange[1].fetch_order_book(sym) for exchange in EXCHANGES])

def get_positive_accounts(balance):
    result = {}
    currencies = list(balance.keys())
    for currency in currencies:
        if balance[currency] and balance[currency] > 0:
            result[currency] = balance[currency]
    return result

def place_order(exchange, symbol, side, amount, _type='limit', price=10.0, stop_price=False, test=True):
    '''
    side: buy | sell
    _type: limit | market | StopLimit | Stop
    '''
    params = { 'test': test, 'stop_price': stop_price }
    order = exchange.create_order(symbol, _type, side, amount, price, params)
    print(order)

def fetch_ohlc(exchange, symbol, timeframe):
    '''
    Timeframes:
    '1m': '1minute',
    '1h': '1hour',
    '1d': '1day',
    '1M': '1month',
    '1y': '1year',
    '''
    try:
        if exchange.has['fetchOHLCV']:
            ohlc = exchange.fetch_ohlcv(symbol, timeframe)
            ohlc = array(ohlc)
            ohlc = ohlc.transpose()
            ohlc = {'time': ohlc[0], 'open': ohlc[1], 'high': ohlc[2], 'low': ohlc[3], 'close': ohlc[4], 'volume': ohlc[5]}
            df = DataFrame(ohlc)
            df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x/1000.0))
            df = df.set_index('time')
            return df
        else:
            print(colored.red('%s doesn\'t support OHLCV' % e))
    except Exception as err:
        print(colored.red(err))

def fetch_orders(exchange):
    return exchange.fetch_orders()

def fetch_order(exchange, id):
    return exchange.fetch_order(id)

def withdraw(exchange, sym, amnt, addr):
    withdraw = exchange.withdraw(sym, amnt, addr)
    print(withdraw)

def generate_crypto_timeframes(exchange, name):
    try:
        tfs = exchange.timeframes.keys()
        df = DataFrame([k for k in tfs])
        to_pickle(df, join('ccxt', 'tfs'), name)
        print(colored.green(name))
    except AttributeError:
        pass
    except HTTPError:
        pass
    except Exception as err:
        print(colored.red(err))

def generate_crypto_symbols(exchange, name):
    try:
        syms = exchange.load_markets()
        out = [key for key in syms]
        df = DataFrame(out)
        to_pickle(df, join('ccxt', 'symbols'), name)
        print(colored.green(name))
        for i in range(len(out)):
            df = DataFrame(syms[out[i]])
            to_pickle(df, join('ccxt', 'conditions'), '{}_{}'.format(name, out[i].replace('/', '_')))
            print(colored.green(out[i]))
    except HTTPError:
        pass
    except Exception as err:
        print(colored.red(err))

def get_syms(e):
    try:
        return [s[0] for s in get_pickle(join('ccxt', 'symbols'), e[0], as_is=True).values]
    except FileNotFoundError:
        pass

def get_tfs(e):
    try:
        return [s[0] for s in get_pickle(join('ccxt', 'tfs'), e[0], as_is=True).values]
    except FileNotFoundError:
        pass

def download_all_crypto(first=False):
    for e in EXCHANGES:
        if first:
            generate_crypto_timeframes(exchange=e[1], name=e[0])
            generate_crypto_symbols(exchange=e[1], name=e[0])

        syms = get_syms(e=e)
        tf = get_tfs(e=e)
        
        if (tf is not None) & (syms is not None):
            for s in syms:
                for t in tf:
                    data = fetch_ohlc(exchange=e[1], symbol=s, timeframe=t)
                    if data is not None:
                        to_pickle(data, 'ccxt', '{}_{}_{}'.format(e[0], s.replace('/', '_'), t))
                        print(colored.green('%s %s %s' % (e[0], s, t)))
