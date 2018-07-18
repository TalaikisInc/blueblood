from os import getenv

from alpha_vantage.timeseries import TimeSeries


def intraday():
    ts = TimeSeries(key=getenv('ALPHAVANTAGE_API_KEY'), output_format='pandas', indexing_type='date')
    data, meta_data = ts.get_intraday('GOOGL')

def sector():
    sp = SectorPerformances(key=getenv('ALPHAVANTAGE_API_KEY'), output_format='pandas')
    data, meta_data = sp.get_sector()
