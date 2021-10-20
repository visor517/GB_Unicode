# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового
# представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).

arr = [
    'разработка',
    'администрирование',
    'protocol',
    'standard',
]

for item in arr:
    strEncode = item.encode('utf-8')
    print(f"bytes:{strEncode} str:{strEncode.decode('utf-8')}")
