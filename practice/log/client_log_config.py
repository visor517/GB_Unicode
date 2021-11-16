import logging
import logging.handlers
import os


LOGGER = logging.getLogger('client')

formatter = logging.Formatter(
    "%(asctime)s %(levelname)-10s %(filename)s %(message)s")

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

fh = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf8', interval=1)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

LOGGER.addHandler(fh)
LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
