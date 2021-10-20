# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и
# длину соответствующих переменных.

arr = [
    b'class',
    b'function',
    b'method',
]

for item in arr:
    print(f'{item} Тип: {type(item)} Длина: {len(item)}')
