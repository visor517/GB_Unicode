# 2 Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о
# заказах. Написать скрипт, автоматизирующий его заполнение данными.

import json

def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r+') as json_file:
        obj = json.load(json_file)
        obj['orders'].append({
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        })
        json_file.seek(0)
        json.dump(obj, json_file, indent=4)

write_order_to_json('Item', 2, 500, 'someone', '22-10-2021')
