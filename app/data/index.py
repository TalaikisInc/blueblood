from backtrader.feeds import DataBase, GenericCSVData


class PandasData(DataBase):
    params = (
        ('datetime', 0),
        ('open', 0),
        ('high', 1),
        ('low', 2),
        ('close', 3),
        ('volume', 4),
        ('openinterest', None)
    )

class PandasTickData(DataBase):
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 1),
        ('low', 1),
        ('close', 1),
        ('volume', 3),
        ('openinterest', -1)
    )

class BidAskCSV(GenericCSVData):
    linesoverride = True
    lines = ('bid', 'ask', 'datetime')
    params = (
        ('datetime', 0),
        ('bid', 1),
        ('ask', 2)
    )
