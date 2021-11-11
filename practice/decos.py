import sys
import logging
import log.server_log_config
import log.client_log_config

if sys.argv[0].find('server') != -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')

def log(func):
    def decorator(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.info(f'Функция: {func.__name__}, Аргументы: {args} {kwargs}')
        return res
    return decorator