from argparse import ArgumentParser
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))
# Db
from app.db import migrate, create_migrations
# Data
from app.data.fred import run_fred
from app.data.iex import iex_symbols, run_iex #, get_spread
from app.data.eod import eod_symbols, run_eod
from app.data.morningstar import run_morningstar
from app.data.tiingo import run_tiingo, tii_symbols, tii_news, save_one
from app.data.gf import run_gf
from app.data.stooq import run_stooq
from app.data.coinmarketcap import get_capitalization
from app.data.fxcm import run_fxcm
from app.data.local import cleaner
# Playground
from app.playground import run_play
# Models
from app.models.alpha import create_owners
from app.models.clusters import make_clusters
#from app.models.risk import ideal_portfolio
# Stats
from app.stats import run_analyze
# Testing
from app.backtest import basic_runs, see_portfolios, run_alpha_strategy
from app.strategies import run_old_strategies, run_bt_strategy
# Utils
from app.utils import easify_names, convert_to_parq, resample_all, convert_mt_pickle

parser = ArgumentParser(description="BlueBlood management point.")
parser.add_argument('--collect')
parser.add_argument('--play')
parser.add_argument('--analyze')
parser.add_argument('--strategy')
parser.add_argument('--convert')
parser.add_argument('--portfolio')
parser.add_argument('--db')
parser.add_argument('--get')
parser.add_argument('--portfolios')
parser.add_argument('--risk')
args = parser.parse_args()

if __name__ == '__main__':
    if args.get:
        save_one(args.get)

    if args.collect:
        #run_fred()
        #get_capitalization()
        if args.collect == 'one_time':
            #iex_symbols()
            #eod_symbols()
            #create_owners()
            tii_symbols()
            #make_clusters()
        # run_iex()
        # get_spread()
        #run_eod()
        #run_gf()
        #run_morningstar()
        #run_stooq()
        run_tiingo()
        #tii_news()
        # sify_names()
        # convert_to_parq()
        # resample_all()
        # run_fxcm()
        # cleaner()

    if args.play:
        run_play(args.play)

    #if args.risk:
        #ideal_portfolio()

    if args.analyze:
        run_analyze(args.analyze)

    if args.strategy:
        if args.strategy == 'bt':
            run_bt_strategy()
        if args.strategy == 'old':
            run_old_strategies()
        #if args.strategy == 'ticks':
            #tick_tester()
        try:
            m = int(args.strategy)
            run_alpha_strategy(m)
        except:
            pass

    if args.convert:
        convert_mt_pickle()

    if args.portfolio:
        basic_runs()

    if args.portfolios:
        see_portfolios()

    if args.db:
        if args.db == 'create_migrations':
            create_migrations()
        if args.db == 'migrate':
            migrate()
