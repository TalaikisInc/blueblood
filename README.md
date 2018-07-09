<p align="center">
  <a href="https://blueblood.ltd/">
    <img alt="Bkue Blood" src="https://github.com/BlueBloodLtd/blueblood.ltd/blob/master/media/logo.png" width="685">
  </a>
</p>

# Blue Blood Engine

Blue Blood Engine is a set of trading related tools and other software.

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
* collect=one_time - 

### R&D

* play=script - run the specified script from playground.
* analyze=factor - analyze specified alpha factor.

### Tests

...

## License

GPL v3.0
