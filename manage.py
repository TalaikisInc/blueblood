from argparse import ArgumentParser
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))
from clint.textui import colored
from stopwatch import StopWatch, format_report
sw = StopWatch()

# Db
from app.db import migrate, create_migrations
# Data
from app.data import (run_fred, eod_symbols, run_eod, run_tiingo, tii_symbols, tii_news, run_quandl, download_eurex,
    save_one, iex_symbols, run_iex, get_capitalization, run_fxcm, get_crypto_balances, download_numerai_dataset,
    upload_predictions, cboe_download, download_futures, process_fundamentals)
# Playground
from app.playground import run_play
# Models
from app.models.alpha import create_owners
from app.models.clusters import make_clusters
from app.portfolio import generate_portfolios
from app.models.numerai import run_numerai_solutions
from app.models import run_derivatives
# Indicators
from app.indicators import generate_indicators
# Watchdogs
from app.watchdogs import run_watchdogs, collect_watchers, clean_storage
# Stats
from app.stats import run_analyze
# Testing
from app.backtest import basic_runs, see_portfolios, run_alpha_strategy
from app.strategies import run_old_strategies, run_bt_fx_ticks, run_bt_pair_strategy, generate_strategies
# Utils
from app.utils import (easify_names, convert_to_parq, resample_all, resample_dukas_all, convert_mt_pickle,
    parq_to_csv_all, pickle_to_csv_all, ensure_correctness)

parser = ArgumentParser(description="BlueBlood management point.")
parser.add_argument('--collect')
parser.add_argument('--play')
parser.add_argument('--analyze')
parser.add_argument('--strategy')
parser.add_argument('--convert')
parser.add_argument('--resample')
parser.add_argument('--portfolio')
parser.add_argument('--db')
parser.add_argument('--get')
parser.add_argument('--trade')
parser.add_argument('--gen')
parser.add_argument('--numerai')
parser.add_argument('--watch')

args = parser.parse_args()

def prepare():
    with sw.timer('prepare'):
        clean_storage()
        print(colored.yellow('Storage cleaned.'))
        collect_watchers()
        print(colored.yellow('Watchers collected.'))
        cboe_download()
        print(colored.yellow('CBOE data downloaded.'))
        run_fred()
        print(colored.yellow('FRED data downloaded.'))
        run_quandl()
        print(colored.yellow('Quandl data downloaded.'))
        generate_indicators()
        print(colored.yellow('Indicators geerated.'))
        generate_portfolios()
        print(colored.yellow('Portfolios geerated.'))
        generate_strategies()
        print(colored.yellow('Strategies geerated.'))
    print(format_report(sw.get_last_aggregated_report()))

if __name__ == '__main__':
    if args.get:
        save_one(args.get)

    if args.collect:
        if args.collect == 'cboe':
            cboe_download()

        if args.collect == 'fund':
            process_fundamentals()

        if args.collect == 'eurex':
            download_eurex()

        if args.collect == 'futures':
            download_futures()
            run_derivatives()

        if args.collect == 'fred':
            run_fred()

        if args.collect == 'quandl':
            run_quandl()

        if args.collect == 'crypto':
            get_capitalization()

        if args.collect == 'one_time':
            #iex_symbols()
            #eod_symbols()
            #create_owners()
            tii_symbols()

        if args.collect == 'iex':
            run_iex()

        if args.collect == 'eod':
            run_eod()

        if args.collect == 'tiingo':
            run_tiingo()

        if args.collect == 'tiingo_news':
            tii_news()

        if args.collect == 'fxcm':
            run_fxcm()
    
    if args.gen:
        generate_indicators()
        generate_portfolios()

    if args.play:
        ''' Various experimental functions to pay before deployment. '''
        run_play(args.play)

    if args.watch:
        prepare()
        run_watchdogs()

    if args.trade:
        if args.trade == 'balance':
            get_crypto_balances()

    if args.analyze:
        run_analyze(args.analyze)

    if args.strategy:
        generate_strategies()
        if args.strategy == 'bt':
            # run_bt_pair_strategy()
            run_bt_fx_ticks()

        if args.strategy == 'old':
            run_old_strategies()

        #if args.strategy == 'ticks':
            #tick_tester()
        try:
            m = int(args.strategy)
            run_alpha_strategy(m)
        except:
            pass

    if args.resample:
        if args.resample == 'dukas':
            resample_dukas_all()

        if args.resample == 'tiingo':
            resample_all()
            ensure_correctness()

    if args.convert:
        if args.convert == 'mt_pickle':
            ''' Converts Metatrader 4 folder csv to pickle.'''
            convert_mt_pickle()

        if args.convert == 'parq_csv':
            ''' Converts parquet to csv.'''
            parq_to_csv_all()

        if args.convert == 'csv_parq':
            ''' Converts go-dukas generated CSV to parquet.'''
            easify_names()
            convert_to_parq()

        if args.convert == 'pickle_csv':
            pickle_to_csv_all()

    if args.portfolio:
        if args.portfolio == 'cluster':
            make_clusters()

        if args.portfolio == 'examine':
            ''' Examine created portfolios (in sampel only). '''
            see_portfolios()

        ''' deprecated. '''
        #basic_runs()

    if args.numerai:
        download_numerai_dataset()
        run_numerai_solutions()
        upload_predictions()

    if args.db:
        if args.db == 'create_migrations':
            create_migrations()
        if args.db == 'migrate':
            migrate()
