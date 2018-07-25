from os.path import join

from logbook import FileHandler, info

from app.utils STORAGE_PATH


def get_log(extra=''):
    if extra != '':
        res = FileHandler(join(STORAGE_PATH, 'logs', 'log.log'), filter=lambda r, h: r.extra[extra])
        with res:
            info('', extra={extra: True})
    else:
        res = FileHandler(join(STORAGE_PATH, 'logs', 'log.log'), bubble=True)
        with res:
            info('')

# @TODO
# https://github.com/getlogbook/logbook/blob/develop/docs/setups.rst