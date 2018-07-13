import sys
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

def create_tables():
    DB.connect()
    DB.create_tables([
        RedditKeyword,
        RedditComment,
        CryptoExchange,
        CryptoMarket,
        Block,
        Address,
        Contract,
        Exchange,
        Market,
        AlphaOwner,
        Strategy,
        Stats,
        Alpha,
        Source,
        News
    ])

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
    'News'
    ]
