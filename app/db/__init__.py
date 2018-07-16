import sys
from importlib import import_module
from os.path import abspath, join, dirname
sys.path.append(abspath(join(dirname(dirname(__file__)), "..")))

from .base import BaseModel, DB
from .blocks import Block
from .contracts import Address, Contract
from .crypto import CryptoExchange, CryptoMarket
from .reddit import RedditComment, RedditCommentCount, RedditKeyword
from .symbols import Exchange, Market, get_exchange, TypeChoices, Index
from .alphas import AlphaOwner, Strategy, Stats, Alpha
from .news import Source, News
from app.utils import filenames


def get_last():
    path = join(dirname(__file__), 'migrations')
    fs = filenames(path)
    no = 1
    for f in fs:
        if '__init__' not in f:
            tmp = int(f.split('_')[0])
            if tmp > no:
                no = tmp
    return no

def create_migrations():
    path = join(dirname(__file__), 'migrations')
    no = get_last() + 1
    fl = open(join(path, '{}_migrations.py'.format(no)), 'w+')
    fl.close()

def migrate():
    no = get_last()
    path = '{}_migrations.py'.format(no)
    module_name = 'app.db.migrations.{}'.format(path.split('.')[0])
    imported_module = import_module(module_name, package='blueblood')
    imported_module.migrate()

__all__ = [
    'BaseModel',
    'DB',
    'Block',
    'Address',
    'Contract',
    'CryptoExchange',
    'CryptoMarket',
    'RedditKeyword',
    'RedditComment',
    'RedditCommentCount',
    'create_tables',
    'Exchange',
    'Strategy',
    'AlphaOwner',
    'Market',
    'Stats',
    'Alpha',
    'get_exchange',
    'TypeChoices',
    'Source',
    'News',
    'create_migrations',
    'migrate'
    ]
