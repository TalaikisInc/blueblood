from os.path import abspath, join, dirname
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), "..")))

import ccxt
from clint.textui import colored as chalk
from peewee import IntegrityError

from models import DB, CryptoExchange, CryptoMarket
from variables.data import EXCHANGES

def put_exchanges():
    for e in ccxt.exchanges:
        print(e)
        try:
            if e is not None:
                CryptoExchange.create(title=e)
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(chalk.red(err))

def insert_market(exchange, name):
    for market in  exchange.load_markets():
        print(market)
        try:
            CryptoMarket.create(market=market, exchange=CryptoExchange.get(title=name).id)
        except IntegrityError:
            DB.rollback()
        except Exception as err:
            print(chalk.red(err))

def get_exchanges():
    return [e.title for e in CryptoExchange.select()]

def get_markets(exchange):
    id = CryptoExchange.get(CryptoExchange.title == exchange)
    markets = CryptoMarket.select().where(CryptoMarket.exchange == id.id)
    return [m.market for m in markets]

def put_markets():
    for exchange in EXCHANGES:
        print(chalk.green(exchange[0]))
        insert_market(exchange=exchange[1], name=exchange[0])

def get_quote():
    for exchange in EXCHANGES:
        for instrument in get_markets(exchange=exchange[0]):
            try:
                print(instrument)
                return exchange[1].fetch_ticker(instrument)
            except Exception as err:
                print(chalk.red(err))
