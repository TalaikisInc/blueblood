from backtrader.feeds import DataBase


class PandasData(DataBase):
    params = (
        ('datetime', None),
        ('open', 'Open'),
        ('high', 'High'),
        ('low', 'Low'),
        ('close', 'Close'),
        ('volume', 'Volume'),
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
