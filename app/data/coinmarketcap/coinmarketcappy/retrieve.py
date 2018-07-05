import requests
from .utils import write_to_file
from .utils import epoch_to_date

BASE_URL = 'https://api.coinmarketcap.com/v1/'


def get_tickers(start=None, limit=None, convert=None, epoch=False, out_file=None, wformat='json'):
    """
    Retrieves all specified tickers

    :param start: int of rank to start retrieving from. Zero indexed
    :param limit: number of tickers to retrieve
    :param convert: if omitted only USD prices are returned. Supported currencies are: "AUD", "BRL", "CAD", "CHF",
        "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR",
        "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
    :param epoch: True if you want the dates returned to be in epoch format, False if you want datetime format
    :param out_file: if provided, info will be saved to this file (local file name or absolute path)
    :param wformat: format to use when writing to output file ('json' by default)
    :return: a list of dictionaries organized by rank. All dictionaries have the following keys:
        id, name, symbol, rank, price_usd, price_btc, 24h_volume_usd, market_cap_usd, available_supply,
        total_supply, max_supply, percent_change_1h, percent_change_24h, percent_change_7d, last_updated

        In addition if the 'convert' argument is specified the following keys will also be available for each dict:
        price_eur, 24h_volume_eur, market_cap_eur (substitute 'eur' with the lower case currency used for 'convert')
    """
    url = '{}ticker/'.format(BASE_URL)
    if limit or convert or start:
        url += '?'
    if start:
        url += 'start={}'.format(start)
    if limit:
        url += '&limit={}'.format(limit)
    if convert:
        url += '&convert={}'.format(convert)

    response = requests.get(url)
    json_response = response.json()

    if not epoch:
        for entry in json_response:
            # * 1000 since method takes in milliseconds
            entry['last_updated'] = epoch_to_date(int(entry['last_updated']) * 1000)

    if out_file:
        write_to_file(json_response, out_file, wformat, tickers=True)
    return json_response


def get_ticker(name=None, convert=None, epoch=False, out_file=None, wformat='json'):
    """
    Retrieves one specific ticker

    :param name: name of the parameter to retrieve. e.g. bitcoin (not btc), ripple (not xrp)...
    :param convert: if omitted only USD prices are returned. Supported currencies are: "AUD", "BRL", "CAD", "CHF",
        "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR",
        "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
    :param epoch: True if you want the dates returned to be in epoch format, False if you want datetime format
    :param out_file: if provided, info will be saved to this file (local file name or absolute path)
    :param wformat: format to use when writing to output file ('json' by default)
    :return: a dictionary with the following keys:
        id, name, symbol, rank, price_usd, price_btc, 24h_volume_usd, market_cap_usd, available_supply,
        total_supply, max_supply, percent_change_1h, percent_change_24h, percent_change_7d, last_updated

        In addition if the 'convert' argument is specified the following keys will also be available for each dict:
        price_eur, 24h_volume_eur, market_cap_eur (substitute 'eur' with the lower case currency used for 'convert')
    """
    url = '{}ticker/{}/'.format(BASE_URL, name)
    if convert:
        url = '{}?convert={}'.format(url, convert.casefold())

    response = requests.get(url)
    json_response = response.json()[0]

    if not epoch:
        # * 1000 since method takes in milliseconds
        json_response['last_updated'] = epoch_to_date(int(json_response['last_updated']) * 1000)

    if out_file:
        write_to_file(json_response, out_file, wformat, simple=True)
    return json_response


def get_global_data(convert=None, out_file=None, epoch=False, wformat='json'):
    """
    Retrieves all available current global data

    :param convert: if omitted only USD prices are returned. Supported currencies are: "AUD", "BRL", "CAD", "CHF",
        "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR",
        "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"
    :param out_file: if provided, info will be saved to this file (local file name or absolute path)
    :param epoch: True if you want the dates returned to be in epoch format, False if you want datetime format
    :param wformat: format to use when writing to output file ('json' by default)
    :return: a dictionary with the following keys:
        total_market_cap_usd, total_24h_volume_usd, bitcoin_percentage_of_market_cap, active_currencies,
        active_assets, active_markets, last_updated

        In addition if the 'convert' argument is specified the following keys will also be available:
        total_market_cap_eur, total_24h_volume_eur
    """
    url = '{}global/'.format(BASE_URL)
    if convert:
        url = '{}?convert={}'.format(url, convert.casefold())

    response = requests.get(url)
    json_response = response.json()

    if not epoch:
        json_response['last_updated'] = epoch_to_date(int(json_response['last_updated']) * 1000)

    if out_file:
        write_to_file(json_response, out_file, wformat, simple=True)
    return json_response
