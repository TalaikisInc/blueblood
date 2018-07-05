import time
import json
from datetime import datetime


def epoch_to_date(date=None):
    """
    Converts the epoch time to date and time

    :param date: epoch in milliseconds to convert
    :return: date in the format '%Y-%m-%d %H:%M:%S'
    """
    if date is None:
        ValueError('Please enter an epoch time to convert to date')
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date/1000))


def start_end(start=None, end=None, url=None):
    """
    Checks to make sure that either start/end are both specified or neither is specified and concatenates
    them with the provided url

    :param start: time as an epoch in milliseconds (if you're not sure just add 3 zeros at the end) or a datetime
        object or a string in the format yyyy-mm-dd[-hh-mm-ss] (hours, minutes and second optional and in most cases
        won't be used)
    :param end: time as an epoch in milliseconds (if you're not sure just add 3 zeros at the end) or a datetime
        object or a string in the format yyyy-mm-dd[-hh-mm-ss] (hours, minutes and second optional and in most cases
        won't be used)
    :param url: base url to concatenate start and end with
    :return: url/start/end/
    """
    # Checks to make sure that either start/end are both specified or neither is specified
    if start and end:
        # start and end parameters are evaluated separately to allow for different input formats if needed
        if type(start) == int:
            pass
        elif type(start) == datetime:
            start = int(time.mktime(start.timetuple())) * 1000
        else:
            temp_start = start.split('-')
            if (len(temp_start) >= 3) and (len(temp_start) <= 6):
                start = int(time.mktime(datetime(*map(int, temp_start)).timetuple())) * 1000
            else:
                raise ValueError('Please enter a valid format for the start date (e.g. yyyy-mm-dd-hh-mm-ss).')

        if type(end) == int:
            pass
        elif type(end) == datetime:
            end = int(time.mktime(end.timetuple())) * 1000
        else:
            temp_end = end.split('-')
            if (len(temp_end) >= 3) and (len(temp_end) <= 6):
                end = int(time.mktime(datetime(*map(int, temp_end)).timetuple())) * 1000
            else:
                raise ValueError('Please enter a valid format for the end date (e.g. yyyy-mm-dd-hh-mm-ss).')

        dates = '{}/{}/'.format(start, end)

    elif not (start and end):
        dates = None
    else:
        raise ValueError('When providing a date range, a start and end must both be provided.')

    if dates is None:
        final_url = url
    else:
        final_url = url + dates

    return final_url


def export_csv(data=None, file=None, simple=False, cmplex=False, tickers=False):
    write_to_file(data, file, wformat='csv', simple=simple, cmplex=cmplex, tickers=tickers)


def export_json(data=None, file=None, simple=False, cmplex=False, tickers=False):
    write_to_file(data, file, wformat='json', simple=simple, cmplex=cmplex, tickers=tickers)


def write_to_file(data=None, file=None, wformat='json', simple=False, cmplex=False, tickers=False):
    """
    Writes json or csv data to file

    :param data: json format data to write to file
    :param file: file to write to (local file or absolute path to file)
    :param wformat: format to write to file on
    :param simple: only set to True when writing a simple list or dict to csv
    :param cmplex: only set to True when writing complex structures (dict with a list of lists as value)
    :param tickers: only set to True when writing multiple tickers
    :return: None
    """
    if data is None:
        raise Exception('Data missing. Please specify the data to write to file.')
    if file is None:
        raise Exception('File name missing. Please specify the name of a file to write to.')

    if not file.endswith('.{}'.format(wformat)):
        file += '.{}'.format(wformat)

    if wformat == 'json':
        with open(file, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    elif wformat == 'csv':
        with open(file, 'w') as f:
            f.write(json_to_csv(data, simple, cmplex, tickers))
    else:
        raise ValueError("Please enter a valid wformat. Valid values are 'json' and 'csv'.")


def read_historical_snaps(file=None, rformat='json'):
    """
    Reads from file and converts to json format if it isn't already

    :param file: file to read from (local file or absolute path to file)
    :param rformat: format of the file
    :return: the data retrieved from file
    """
    if file is None:
        raise Exception('File name missing. Please specify the name of a file to read from.')

    if not file.endswith('.{}'.format(rformat)):
        file += '.{}'.format(rformat)

    if rformat == 'json':
        with open(file, 'r') as f:
            contents = f.read()
            return json.loads(contents)
    elif rformat == 'csv':
        with open(file, 'r') as f:
            contents = f.read()
            contents = csv_to_json(contents)
            return contents
    else:
        raise ValueError("Please enter a valid rformat. Valid values are 'json' and 'csv'.")


def json_to_csv(data=None, simple=False, cmplex=False, tickers=False):
    """
    Specify data to convert to csv format (not both)

    :param data: json formatted data to convert to csv format
    :param simple: only set to True when writing a simple list or dict to csv
    :param cmplex: only set to True when writing complex structures (dict with a list of lists as value)
    :param tickers: only set to True when writing the multiple tickers
    :return: csv format data
    """
    if data is None:
        raise ValueError('Data missing. Please specify the data to convert.')

    # write data as a table in csv. top row contains headers, first one being 'dates'
    if cmplex:
        output = 'date,'
        temp = data.popitem()
        output += temp[0] + '\n'
        for x in temp[1]:
            output += ','.join(map(str, x)) + '\n'
        output = output.split('\n')
        for x in data:
            output[0] = ','.join([output[0], x])
            for i, y in enumerate(data[x]):
                output[i+1] = ','.join([output[i+1], str(y[1])])
        return '\n'.join(output)

    output = ''
    if simple:
        if type(data) == list:
            output = '\n'.join(data)
        elif type(data) == dict:
            keys = data.keys()
            output += ','.join(keys) + '\n'
            output += ','.join(str(data[x]) for x in keys) + '\n'
        else:
            raise ValueError('Only set the parameter "simple" to True when writing a simple'
                             ' (nothing nested) list or dict.')
        return output

    if tickers:
        keys = data[0].keys()
        output += ','.join(keys) + '\n'
        for entry in data:
            output += ','.join(str(entry[x]) for x in keys) + '\n'
        return output

    # Organizes the dates so that the output csv file is properly organized as well
    keys = list(data.keys())
    keys.sort()

    # Goes through each date (outer loop) and each rank (inner) to convert to csv format
    for x in keys:
        output += x + '\n'
        for y in data[x]:
            output += ','.join(map(str, y)) + '\n'
    return output


def csv_to_json(data=None):
    """
    Takes properly formatted csv data and returns it in json format

    :param data: csv formatted data to convert to json format
    :return: json format data
    """
    if data is None:
        raise ValueError('Data missing. Please specify the data to convert.')

    converted = dict()
    base = None
    for line in data.splitlines():
        split = [x.strip() for x in line.split(',')]
        if len(split) == 1:
            base = split[0]
            converted[base] = list()
        else:
            converted[base].append(split)
    return converted
