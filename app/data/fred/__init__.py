from os.path import join, dirname, abspath
import sys
sys.path.append(abspath(join(dirname(dirname(__file__)), '..')))

from .index import run
