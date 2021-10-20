# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

arr = [
    'attribute',
    'класс',
    'функция',
    'type',
]

for item in arr:
    try:
        bytesItem = f"b'{item}'"
        eval(bytesItem)
    except SyntaxError:
        print(f'Слово \"{item}\" невозможно записать в байтовом типе.')
