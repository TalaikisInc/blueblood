<p align="center">
  <a href="https://blueblood.ltd/">
    <img alt="Bkue Blood" src="https://github.com/BlueBloodLtd/blueblood.ltd/blob/master/media/logo.png" width="685">
  </a>
</p>

# Blue Blood Engine

Blue Blood Engine is a set of trading related tools and other software.

## STATUS

In active development, what means not every module will or should work.

## Note

This repo probably wouldn't be usable without models/ directory, which is proprietary and wouldn't be disclosed (at least currently).


## Predecessor

This project is the child, totally not compatible next generation of the [Quantrade](https://github.com/quant-trade/Quantrade) project.

## Install

```bash
chmod +x env.sh
./env.sh
```

Or, just use Docker:

```bash
chmod +x build.sh
chmod +x run.sh
./build.sh
./run.sh
```

## Start

Edit .env, create (Postgres) database 'blueblood', then:

```bash
python manage.py --db=one_time
cd db
node makeTables.js
```


## Modules

1. Data collection.
2. Alpha models.
3. Risk models.
4. Index models.
5. Execution models.
6. Statistics.
7. Watchdogs.

## Management

Single point management:

```bash
python manage.py --<sommand>=<params>
```

## Commands

### Initializers

* python manage.py --db=one_time - creates required tables

### Data

* collect=True - collect data for non-daemonized collectors
* collect=one_time - rarely run collections (like sysmbols)

### R&D

* play=script - run the specified script from playground.
* analyze=factor - analyze specified alpha factor.

### Tests

...

### Example of alpha formatting

For alpha providers.

1. Multi-instrument model:

This model runs on portfolio of instruments we provide.

```python
def compute(data, symbols):
    # Who is owner of this alpha:
    owner = Owner('My Name', 'my@email.com>', '')

    # Determine strategy rules, as an example - long above50 quantile, short below 50:
    rule = Rule(('gt', 50), ('lt', 50))

    '''
    Description (optional)
    '''
    for symbol in symbols:
        # your code
        # ...
        # your code
        data[symbol] = #... What you return as a factor for each symbol
    return data
```

2. Pair model:

Pair mdoels are symbol pairs specific alpha models.

```python
def compute(data):
    owner = Owner('Your name', 'your@email.com')
    symbols = [
        Pair('INST1', 'INST2'),
        Pair('INST3', 'INST4'),
    ]

    '''
    Description.
    '''

    for i in range(len(symbols)):
        # ...
        data[symbols[i].symbol_a] = # ...

    return data
```

3. Fixed model:

```python
def compute(data):
    owner = Owner('My name', 'my@email.com')
    inputs = Pair('INS1', 'INS2')
    output = Fixed('TRADE_THIS')

    '''
    Description (optional).
    '''

    data[output.symbol] = # ... what you do for this symbol specific model

    return data
```

### Rules

1. Each factor should return column named symbol, intermediate calcualtions can be dropped.
2. Available data columns are named in following way, example: 'SYMBOL_Close', same for Open, High, Low, Volume, AdjClose, Diff, Pct.
3. Some functions if needed can be found in utils/ or stats/. Otherwise,request them.
4. Each factor will be tested for its uniqueness.

## License

GPL v3.0
