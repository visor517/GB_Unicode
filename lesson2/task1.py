# 1 Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных
# данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.

import csv, re

def get_data(files):
    main_data = [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы',
    ]
    result = [main_data]

    for file_name in files:
        with open(file_name, 'r') as file:
            content = file.read()
        item_data = [] 
        for item in main_data:
            item_data.append(re.search(item + r': +(.+)\n', content)[1])
        result.append(item_data)

    return result

def wrire_to_csv(file):
    data = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])

    with open(file, 'w', newline='') as result_file:
        RES_FILE_WRITER = csv.writer(result_file)
        for row in data:
            RES_FILE_WRITER.writerow(row)

wrire_to_csv('task1.csv')
