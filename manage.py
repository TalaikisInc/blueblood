WITH_CLEANER = False
PRIVATE = True # Set for False for demo purposes


from argparse import ArgumentParser
from os.path import join, dirname, abspath

from dotenv import load_dotenv
load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))
from clint.textui import colored
from stopwatch import StopWatch, format_report
sw = StopWatch()

from app.db import migrate, create_migrations
from app.data import (run_fred, eod_symbols, run_eod, run_tiingo, tii_symbols, tii_news, run_quandl, download_eurex,
    save_one, iex_symbols, run_iex, get_capitalization, run_fxcm, get_crypto_balances, download_numerai_dataset,
    upload_predictions, cboe_download, download_futures, process_fundamentals, download_all_crypto, get_am_vars)
from app.playground import run_play
from app.portfolio import generate_portfolios
if PRIVATE:
    from app.models._private.numerai import run_numerai_solutions
from app.models import run_derivatives
from app.indicators import generate_indicators
from app.watchdogs import run_watchdogs
from app.stats import run_analyze
from app.backtest import basic_runs, see_portfolios, run_alpha_strategy
from app.strategies._private import run_old_strategies, run_bt_fx_ticks, run_bt_pair_strategy
from app.strategies import generate_strategies
from app.utils import (easify_names, convert_to_parq, resample_all, resample_dukas_all, convert_mt_pickle,
    parq_to_csv_all, pickle_to_csv_all, ensure_correctness, clean_storage, collect_used_data, convert_mt_one)
if PRIVATE:
    from app.index import measures_helper, genesis, get_current_weights


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
parser.add_argument('--mt_pickle')
parser.add_argument('--symbols')
parser.add_argument('--am')
args = parser.parse_args()

def prepare():
    with sw.timer('prepare'):
        if WITH_CLEANER:
            clean_storage()
            print(colored.yellow('Storage cleaned.'))
        collect_used_data()
        print(colored.yellow('Data collected.'))
        cboe_download()
        print(colored.yellow('CBOE data downloaded.'))
        download_futures(last=True, forceDownload=True)
        run_derivatives()
        print(colored.yellow('CBOE futures downloaded.'))
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
    
    if args.am:
        get_am_vars()

    if args.symbols:
        if args.symbols == 'iex':
            iex_symbols()

        if args.symbols == 'eod':
            eod_symbols()

        if args.symbols == 'tiingo':
            tii_symbols()

    if args.collect:
        if args.collect == 'cboe':
            cboe_download()

        if args.collect == 'crypto':
            download_all_crypto()

        if args.collect == 'fund':
            process_fundamentals()

        if args.collect == 'eurex':
            download_eurex()

        if args.collect == 'futures':
            download_futures(forceDownload=True)
            run_derivatives()

        if args.collect == 'fred':
            run_fred()

        if args.collect == 'quandl':
            run_quandl()

        if args.collect == 'crypto':
            get_capitalization()

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
        if args.gen == 'i':
            generate_indicators()

        if args.gen == 'p':
            generate_portfolios()

        if args.gen == 's':
            generate_strategies()
        
        if args.gen == 'x':
            #genesis()
            get_current_weights()
            #measures_helper()

    if args.play:
        ''' Various experimental functions to pay before deployment. '''
        run_play(args.play, private=PRIVATE)

    if args.watch:
        prepare()
        run_watchdogs()

    if args.trade:
        if args.trade == 'balance':
            get_crypto_balances()

    if args.analyze:
        run_analyze(args.analyze)

    if args.strategy:
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

    if args.mt_pickle:
        '''Converts one MT4 symbol to pickle.'''
        convert_mt_one(args.mt_pickle)

    if args.convert:
        if args.convert == 'mt_pickle':
            ''' Converts Metatrader 4 folder csvs to pickle.'''
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
        if args.portfolio == 'examine':
            ''' Examine created portfolios (in sampel only). '''
            see_portfolios()

    if args.numerai:
        download_numerai_dataset()
        run_numerai_solutions()
        upload_predictions()

    if args.db:
        if args.db == 'create_migrations':
            create_migrations()
        if args.db == 'migrate':
            migrate()
