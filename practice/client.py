"""Программа-клиент"""

import json
import socket
import sys
import time
import threading
import logging
import log.client_log_config
import argparse
from decos import log

from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, PORT, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT, RECIVER

LOGGER = logging.getLogger('client')


@log
def create_presence(server_port, my_name):
    """Генерирует запрос о присутствии клиента"""
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: server_port,
        USER: {
            ACCOUNT_NAME: my_name
        }
    }
    return out

@log
def create_message(sock, my_name):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""

    while True:
        message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
        if message == '!!!':
            sock.close()
            LOGGER.info('Завершение работы по команде пользователя.')
            print('Спасибо за использование нашего сервиса!')
            time.sleep(1)
            break
        reciver = input('Введите получателя: ')
        message_dict = {
            ACTION: MESSAGE,
            RECIVER: reciver,
            TIME: time.time(),
            ACCOUNT_NAME: my_name,
            MESSAGE_TEXT: message
        }
        LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(sock, message_dict)
            LOGGER.info(f'Отправлено сообщение для пользователя {reciver}')
        except:
            LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)

@log
def recive_message(sock, my_name):
    """Обработчик сообщений поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and MESSAGE_TEXT in message and \
                    RECIVER in message and message[RECIVER] == my_name:
                print(f'\n{message[SENDER]}: {message[MESSAGE_TEXT]}')
                LOGGER.info(f'Пользователь {my_name} получил сообщение от {message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

        except:
            LOGGER.critical(f'Потеряно соединение с сервером.')
            break

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
    parser.add_argument('-n', '--name', default='Guest', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_ip = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    if not 1024 < server_port < 65535:
        LOGGER.critical(f'Введено недопустимое значение порта сервера: {server_port}')
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    
    return server_ip, server_port, client_name

def main():
    server_ip, server_port, client_name = arg_parse()
    LOGGER.info(f'Клиент {client_name} формирует запрос к серверу: {server_ip} {server_port}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_ip, server_port))
        send_message(transport, create_presence(server_port, client_name))
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
        print(f'Запущен клиент {client_name}')

        # процесс приема
        receiver = threading.Thread(target=recive_message, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # процесс отправки
        sender = threading.Thread(target=create_message, args=(transport, client_name))
        sender.daemon = True
        sender.start()
        LOGGER.debug('Запущены процессы')
    
        # цикл работы клиента и условие завершения
        while True:
            time.sleep(1)
            if not receiver.is_alive() or not sender.is_alive():
                break

if __name__ == '__main__':
    main()
