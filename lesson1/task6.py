# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в
# формате Unicode и вывести его содержимое.

from chardet import detect

lines = [
    'сетевое программирование',
    'сокет',
    'декоратор',
]

with open('test_file.txt', 'w') as file:
    for line in lines:
        file.write(line + '\n')

with open('test_file.txt', 'rb') as file:
    text = file.read()
ENCODING = detect(text)['encoding']
print(ENCODING)

with open('test_file.txt', 'r', encoding=ENCODING) as file:

    print(file.read())
