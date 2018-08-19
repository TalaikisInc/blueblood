from os import chdir, getenv
from os.path import join, abspath
from collections import namedtuple


META_PATHS = [
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_AVA_TERMINAL_ID'), 'MQL4', 'Files'),
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_DARWIN_TERMINAL_ID'), 'MQL4', 'Files'),
    join(abspath(chdir('C:\\')), 'Users', getenv('WIN_USER'), 'AppData', 'Roaming', 'MetaQuotes', 'Terminal', getenv('META_XTB_TERMINAL_ID'), 'MQL4', 'Files'),
]

STORAGE_PATH = abspath(chdir('G:\\storage'))
DATA_SOURCE = 'eod'
PER_SAHRE_COM = 0.0035
SEC_FEE = 23.1 # Per $1M
FINRA_FEE = 0.000119 # Per share

Pair = namedtuple('Pair', 'symbol_a symbol_b')
Owner = namedtuple('Owner', 'name email')
Fixed = namedtuple('Fixed', 'symbol')
LongRule = namedtuple('LongRule', 'op value')
ShortRule = namedtuple('ShortRule', 'op value')

CONSTANT_CAPITAL = 100000
