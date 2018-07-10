from argparse import ArgumentParser
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))

from app.data.fred import run as fred
from app.data.iex import iex_symbols, run_history #, get_spread
from app.data.eod import eod_symbols
from app.data.coinmarketcap import get_capitalization
from app.models.playground import run_play
from app.stats import run_analyze
from app.data.local import convert_mt_pickle
from app.backtest import basic_runs
from app.db import create_tables

parser = ArgumentParser(description="BlueBlood management point.")

parser.add_argument('--collect')
parser.add_argument('--play')
parser.add_argument('--analyze')
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
            eod_symbols()
        #run_history()
        # get_spread()

    if args.play:
        run_play(args.play)

    if args.analyze:
        run_analyze(args.analyze)

    if args.convert:
        convert_mt_pickle()

    if args.portfolio:
        basic_runs()

    if args.db:
        if args.db == 'one_time':
            create_tables()
