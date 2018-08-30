from backtrader.observers import Broker, BuySell, DrawDown, TimeReturn, Trades, Cash


def observers(cerebro):
    cerebro.addobserver(Broker)
    cerebro.addobserver(Cash)
    cerebro.addobserver(BuySell)
    cerebro.addobserver(DrawDown)
    cerebro.addobserver(Trades)
    return cerebro
