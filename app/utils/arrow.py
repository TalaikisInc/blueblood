from os import getenv

from pyarrow import Table
from pyarrow.parquet import write_table, read_table


def to_arrow(df):
    return Table.from_pandas(df)

def to_pandas(table):
    return table.to_pandas()

def read(path):
    return read_table(path, nthreads=getenv('AVAILABLE_CORES'))

def write(table, path):
    write_table(table, path)
