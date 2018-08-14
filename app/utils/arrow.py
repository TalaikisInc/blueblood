from os import getenv
from os.path import join

from pyarrow import Table
from pyarrow.parquet import write_table, read_table

from app.utils.vars import STORAGE_PATH


def to_arrow(df):
    return Table.from_pandas(df)

def to_pandas(table):
    return table.to_pandas()

def read_pa(folder, name):
    return read_table(join(STORAGE_PATH, folder, '{}.paq'.format(name)), nthreads=getenv('AVAILABLE_CORES'))

def write_pa(table, folder, name):
    write_table(table, join(STORAGE_PATH, folder, '{}.paq'.format(name)))
