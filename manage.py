from argparse import ArgumentParser
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))

# Db
from app.db import migrate, create_migrations
# Data
from app.data.fred import run as fred
from app.data.iex import iex_symbols, run_iex #, get_spread
from app.data.eod import eod_symbols, run_eod
from app.data.morningstar import run_morningstar
from app.data.tiingo import run_tiingo, tii_symbols, tii_news
from app.data.gf import run_gf
from app.data.stooq import run_stooq
from app.data.coinmarketcap import get_capitalization
from app.data.fxcm import run_fxcm
from app.data.local import convert_mt_pickle, cleaner
# Models
from app.models.playground import run_play
from app.models.alpha import create_owners
from app.models.clusters import make_clusters
# Stats
from app.stats import run_analyze, run_strategy
# Testing
from app.backtest import basic_runs

parser = ArgumentParser(description="BlueBlood management point.")

parser.add_argument('--collect')
parser.add_argument('--play')
parser.add_argument('--analyze')
parser.add_argument('--strategy')
parser.add_argument('--convert')
parser.add_argument('--portfolio')
parser.add_argument('--db')
args = parser.parse_args()

if __name__ == '__main__':
    if args.collect:
        #fred()
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
        # tii_news()
        run_tiingo()
        # run_fxcm()
        # cleaner()

    if args.play:
        run_play(args.play)

    if args.analyze:
        run_analyze(args.analyze)

    if args.strategy:
        run_strategy(args.strategy)

    if args.convert:
        convert_mt_pickle()

    if args.portfolio:
        basic_runs()

    if args.db:
        if args.db == 'create_migrations':
            create_migrations()
        if args.db == 'migrate':
            migrate()
