from backtrader import CommInfoBase


class ForexCommisionScheme(CommInfoBase):
    '''
    This commission scheme attempts to calcuate the commission hidden in the
    spread by most forex brokers. It assumes a mid point data is being used.
 
    *New Params*
    spread: Float, the spread in pips of the instrument
    two: Bool, states whether the pair being traded is a JPY pair
    acc_counter_currency: Bool, states whether the account currency is the same
    as the counter currency. If false, it is assumed to be the base currency
    '''
    params = (
        ('spread', 2.0),
        ('stocklike', False),
        ('two', False),
        ('acc_counter_currency', True),
        ('commtype', CommInfoBase.COMM_FIXED),
        )
 
    def _getcommission(self, size, price, pseudoexec):
        '''
        If account currency is same as the base currency, change pip value calc.
        '''
        if self.p.two == True:
            multiplier = 0.01
        else:
            multiplier = 0.0001
 
        if self.p.acc_counter_currency == True:
            comm = abs((self.p.spread * (size * multiplier)))
        else:
            comm =  abs((self.p.spread * ((size / price) * multiplier)))
 
        return comm
