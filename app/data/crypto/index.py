from ccxt import exchanges
from clint.textui import colored
from peewee import IntegrityError
from pandas import DataFrame

from app.db import DB, CryptoExchange, CryptoMarket
from app.variables import EXCHANGES


def put_exchanges():
    for e in exchaanges:
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

def get_quote():
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
    ohlc = exchange.fetch_ohlcv(symbol, timeframe)
    return DataFrame(ohlc)

def fetch_orders(exchange):
    return exchange.fetch_orders()

def fetch_order(exchange, id):
    return exchange.fetch_order(id)

def withdraw(exchange, sym, amnt, addr):
    withdraw = exchange.withdraw(sym, amnt, addr)
    print(withdraw)
