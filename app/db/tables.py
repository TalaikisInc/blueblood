from . import (DB, RedditKeyword, RedditComment, CryptoExchange,
    CryptoMarket, Block, Address, Contract, Exchange, Market)


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
        Market
    ])
