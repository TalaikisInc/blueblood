def risk_per_trade_asset(equity, risk=2):
    return equity * risk / 100

def currency_adjust_mt(tick_value, point, tick_size):
    return tick_value * point / tick_size

def lost(equity, risk, tick_value, point, tick_size, sl, decimals=2):
    return round(risk_per_trade_asset(equity, risk) / currency_adjust_mt(tick_value, point, tick_size) / sl, decimals)
