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

```
chmod +x env.sh
./env.sh
pip install -r requirements.txt
```

## Start

Edit .env, create (Postgres) database 'blueblood', then:

```
cd db
node makeTables.js
cd ../models
python create_tables.py
```


## Modules

1. Data collection.
2. Alpha models.
3. Risk models.
4. Index models.
5. Execution models.
6. Statistics.
7. Watchdogs.

## License

GPL v3.0
