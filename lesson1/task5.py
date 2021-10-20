# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
# в строковый тип на кириллице.

import subprocess
import chardet

sites = [
    'yandex.ru',
    'youtube.com',
]

for site in sites:
    YA_PING = subprocess.Popen(['ping', site], stdout=subprocess.PIPE)
    count = 0
    for line in YA_PING.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
        if count > 4:
            break
        count += 1
