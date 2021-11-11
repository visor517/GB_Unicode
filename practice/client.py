"""Программа-клиент"""

import json
import socket
import sys
import time
import logging
import log.client_log_config
from decos import log

from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, PORT, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT

LOGGER = logging.getLogger('client')


@log
def create_message(server_port, account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: server_port,
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out

@log
def check_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    """Загружаем параметы коммандной строки"""
    try:
        server_ip = sys.argv[2]
        server_port = int(sys.argv[1])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_ip = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        LOGGER.critical(
            'В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    LOGGER.info(f'Клиент формирует запрос к серверу: {server_ip} {server_port}')

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_ip, server_port))
    message_to_server = create_message(server_port)
    send_message(transport, message_to_server)
    try:
        answer = check_ans(get_message(transport))
        LOGGER.info(f'Принят ответ от сервера: {answer}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
