# Python CityIndex API

## Introduction
CityIndex API written in Python

## Dependency
This package depends on Python-requests `http://www.python-requests.org/`

## Usage
Note: API is a singleton class.

### Init
```python
api = API(username, password)
```

### Authentication

#### Login
Return `True` or `False`.
Note: The session token will be stored in `api.session`.
```python
api.login()
```


#### Logout
Return `True` or `False`
```python
api.logout()
```

### Account Information

#### Trading Account Information
Result is stored in `api.trading_account_info`
Return `False` if failed.
```python
api.get_trading_account_info()
```

### Margin

#### Get Margin Information
Result is stored in `api.client_account_margin`
Return `False` if failed.
```python
api.get_client_account_margin()
```

### Market Information

#### Get Full Market Information
Result is stored in `api.market_info`
Return `False` if failed.
Click [here for the list of Market Tag ID](http://docs.labs.cityindex.com/#MarketTagIDs.htm%3FTocPath%3DGetting%2520Started%7CLookup%2520Values%7C_____2).  
```python
api.get_full_market_info(market_tag_id)
```

### Prices
#### Price bar history
```python
api.get_pricebar_history(symbol, interval, span, pricebars, priceType)
```

### Trades and orders
#### Simulate Trade Order
```python
api.simulate_trade_order(symbol, cmd, qty, data)
```
#### Place Market Order
```python
api.send_market_order(symbol, cmd, qty, data, stoploss=0.0, takeprofit=0.0):
```
#### Modify Order
```python
api.modify_order(symbol, order, stoploss=0.0, takeprofit=0.0)
```

#### Close Order
```python
api.close_order(symbol, order, data)
```

#### Get Order History
```python
api.get_order_history()
```

#### Get Order
```python
api.get_order(orderID)
```

#### Cross Rate
```python
api.cross_rate(symbol, cmd, data)
```