from numpy import where


def breakout(df, col, op, per):
    assert (op == 'up') | (op == 'dn'), 'Operation should be one of: \'up\', \'dn\', '

    if op == 'up':
        df['mx'] = df[col].rolling(window=per, min_periods=per).max()
        df['sig'] = where(df[col] > df['mx'].shift(), 1, 0)
    if op == 'dn':
        df['mn'] = df[col].rolling(window=per, min_periods=per).min()
        df['sig'] = where(df[col] < df['mn'].shift(), 1, 0)
    return df['sig']
