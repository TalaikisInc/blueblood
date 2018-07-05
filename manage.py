from argparse import ArgumentParser

from app.data.fred import run
from app.data.coinmarketcap import get_capitalization
from app.models.playground import run_play

parser = ArgumentParser(description="BlueBlood management point.")

parser.add_argument('--collect')
parser.add_argument('--play')
args = parser.parse_args()

if args.collect:
    # run()
    get_capitalization()

if args.play:
    run_play(args.play)