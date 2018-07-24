from numpy import where, power, abs


def gpointpow():
    return power(10, 2)

def gpointcoef():
    return 1/gpointpow()

def bearishengulfing(df):
    return where((
        (df['Close'].shift() > df['Open'].shift()) &
        (df['Open'] > df['Close']) &
        (df['Open'] >= df['Close'].shift()) &
        (df['Open'].shift() >= df['Close']) &
        ((df['Open'] - df['Close']) > (df['Close'].shift() - df['Open'].shift()))
    ), 1, 0)

def bbulishengulfing(df):
    return where((
        (df['Open'].shift() > df['Close'].shift()) &
        (df['Close'] > df['Open']) &
        (df['Close'] >= df['Open'].shift()) &
        (df['Close'].shift() >= df['Open']) &
        ((df['Close'] - df['Open']) > (df['Open'].shift() - df['Close'].shift()))
    ), 1, 0)

def ochl()df:
    return where((df['High'] - df['Low']) != 0, (df['Open'] - df['Close']) / (df['High'] - df['Low']), 0)

def darkcloudcover(df):
    return where((
        (df['Close'].shift() > df['open'].shift()) &
        (((df['Close'].shift() + df['Open'].shift()) / 2.0) > df['Close']) &
        (df['Open'] > df['Close']) &
        (df['Close'] > df['Open'].shift()) &
        (ochl(df) > 0.5) &
        ((df['High'] - df['Low']) >= (10 * coef))
    ), 1, 0)

def doji(df):
    return where((
        (abs(df['Open'].shift() - df['Close'].shift()) * gpointpow) < 0.6
    ), 1, 0)

def bodylow(df):
    return where(df['Open'] > df['Close'], df['Close'], df['Open'])

def bodyhigh(df):
    return where(df['Open'] > df['Close'], df['Open'], df['Close'])

def hammer(df):
    return where((
        (((bodylow(df) - df['Low']) / 2.0) > (df['High'] - bodyhigh(df))) &
        (((bodylow(df) - df['Low'])) > abs(df['Open'] - df['Close']) * 0.9) &
        ((df['High'] - df['Low']) >= 12 * gpointcoef()) &
        (df['Open'] != df['Close']) &
        (((bodylow(df) - df['Low']) / 4.0) <= (df['High'] - bodyhigh(df)))
    ), 1, 0)

def cohl(df):
    return where((df['High'] - df['Low'] != 0), (df['Close'] - df['Open']) / (df['High'] - df['Low']), 0)

def piercingline(df):
    return where((
        (df['Close'].shift() < df['Open'].shift()) &
        (((df['Close'].shift() + df['Open'].shift()) / 2.0) < df['Close']) &
        (df['Open'] < df['Close']) &
        (cohl(df) > 0.5) &
        ((df['High'] - df['Low']) > 10 * gpointcoef())
    ), 1, 0)

def shootingstar(df):
    return where((
        (df['High'] > df['High'].shift()) &
        (df['High'] > df['High'].shift(2)) &
        (df['High'] > df['High'].shift(3)) &
        ((df['High'] - bodyhigh(df) / 4.0) > (bodylow(df) - df['Low'])) &
        ((df['High'] - bodyhigh(df) / 4.0) > (abs(df['Open'] - df['Close']) * 0.9)) &
        ((df['High'] df['Low']) >= 12 * (gpointcoef())) &
        (df['Open'] != df['Close'])
    ), 1, 0)
