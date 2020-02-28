<p align="center">
  <a href="https://blueblood.talaikis.com/">
    <img alt="Bkue Blood" src="https://github.com/BlueBloodLtd/blueblood.ltd/blob/master/media/logo.png" width="685">
  </a>
</p>

# Blue Blood Engine

![Structure (not fully implemented)](https://github.com/TalaikisInc/blueblood/blob/master/media/s-index.png)

Blue Blood Engine is a set of trading and analysis related tools and other software.

## Predecessor

This project is the child, not compatible next generation of the [Quantrade](https://github.com/TalaikisInc/Quantrade) project.

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

## Management

Single point management:

```bash
python manage.py --<command>=<params>
```

## Commands

### Initializers

```bash
# creates required tables:
python manage.py --db=one_time
```

### Data

```bash
# collect data for non-daemonized collectors, for parameters - see manage.py:
collect=<param>
# rarely run collections (like sysmbols)
collect=one_time
```

### R&D

```bash
# run the specified script from playground
play=<script>
# playground has a simple demo file, run it:
play=demo
# analyze specified alpha factor.
analyze=<factor>
```

### Tests

...

### Strategy format

Strategies are put inside app/stratrgies/_implementations/ directory.

```python

def main():
    # Your code

    return [[returns_vector, 'name']]

```

### Indicator format

Preprocessed indicators are put inside app/indicators/_implementations/ directory.

```python

def main():
    # Your code

    return [[indicator_vector, 'name']]

```

### Portfolio format

Portfolios are put inside app/portfolio/_implementations/ directory.

```python

def main():
    # Your code

    return [[returns, adjusted_returns, commissions_vector, 'name']]]

```

## License

GPL v3.0
