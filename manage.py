from argparse import ArgumentParser

from app.data.fred import run

parser = ArgumentParser(description="BlueBlood management point.")

parser.add_argument('--collect')
args = parser.parse_args()

if args.collect:
   run()
