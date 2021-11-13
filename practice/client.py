"""Программа-клиент"""

import json
import socket
import sys
import time
import logging
import log.client_log_config
import argparse
from decos import log

from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, PORT, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT

LOGGER = logging.getLogger('client')


@log
def create_presence(server_port, account_name='Guest'):
    """Генерирует запрос о присутствии клиента"""
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
def create_message(sock, account_name='Guest'):
    """
    Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict

@log
def recive_message(message):
    """Обработчик сообщений поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOGGER.info(f'Получено сообщение от пользователя '
                    f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

@log
def check_presence_ans(message):
    """Разбирает ответ сервера на сообщение о присутствии"""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError

@log
def arg_parse():
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_ip = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
    if not 1024 < server_port < 65535:
        LOGGER.critical(f'Введено недопустимое значение порта сервера: {server_port}')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    if client_mode not in ('send', 'recive'):
        LOGGER.critical(f'Введено недопустимое значение режима работы: {client_mode}')
        print('В качестве режима работы можно указывать send, recive')
        sys.exit(1)
    
    return server_ip, server_port, client_mode

def main():
    server_ip, server_port, client_mode = arg_parse()
    LOGGER.info(f'Клиент в режиме {client_mode} формирует запрос к серверу: {server_ip} {server_port}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_ip, server_port))
        send_message(transport, create_presence(server_port))
        answer = check_presence_ans(get_message(transport))
        LOGGER.info(f'Принят ответ от сервера: {answer}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER.error('Не удалось декодировать сообщение сервера.')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER.critical(
            f'Не удалось подключиться к серверу {server_ip}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    else:
        while True:
            try:
                if client_mode == 'send':
                    send_message(transport, create_message(transport))
                elif client_mode == 'recive':
                    recive_message(get_message(transport))

            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                LOGGER.error(f'Соединение с сервером {server_ip} было потеряно.')
                sys.exit(1)

if __name__ == '__main__':
    main()
