from app.db import (DB, Block, Address, Contract, CryptoExchange, CryptoMarket, RedditComment, RedditCommentCount, RedditKeyword,
    Exchange, Market, get_exchange, TypeChoices, Index, AlphaOwner, Strategy, Stats, Alpha, Source, News)


def migrate():
    DB.connect()
    DB.create_tables([
        Address,
        Block,
        Contract,
        Exchange,
        Market,
        Alpha,
        Source,
        News,
        RedditKeyword,
        RedditComment,
        CryptoExchange,
        CryptoMarket,
        Stats,
        Strategy,
        AlphaOwner
    ])
