from os import chdir
from os.path import join, dirname, abspath
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), '...')))

from .split import train_test_split
from .index import periodize_returns, filenames
STORAGE_PATH = abspath(chdir('G:\\storage'))

__ALL__ = [
    'train_test_split',
    'periodize_returns',
    'STORAGE_PATH',
    'filenames'
  ]
