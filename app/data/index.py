from app.backtest.backtrader.feeds import DataBase, GenericCSVData


class PandasData(DataBase):
    params = (
        ('datetime', None),
        ('open', 0),
        ('high', 1),
        ('low', 2),
        ('close', 3),
        ('volume', 4),
        ('openinterest', None)
    )

class PandasTickData(DataBase):
    params = (
        ('datetime', None),
        ('open', 1),
        ('high', 1),
        ('low', 1),
        ('close', 1),
        ('volume', 1),
        ('openinterest', None)
    )

class BidAskCSV(GenericCSVData):
    linesoverride = True
    lines = ('datetime', 'ask', 'bid' )
    params = (
        # (datetime, 0), # inherited from parent class
        ('ask', 1),  # default field pos 1
        ('bid', 2),  # default field pos 2
    )
