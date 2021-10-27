# Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в
# файле YAML-формата. Для этого:

import yaml

DATA_TO_YAML = {
    'yaml-list': ['one','two','three'],
    'yaml-int': 42,
    'yaml-dict': {
        '€': 'euro',
        'Ф': 'f',
        'Ђ': 'no option'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(DATA_TO_YAML, file, default_flow_style = True, allow_unicode = True)

with open('file.yaml', 'r', encoding='utf-8') as yaml_file:
    DATA_FROM_YAML = yaml.load(yaml_file, Loader=yaml.FullLoader)

print(DATA_TO_YAML)
print(DATA_FROM_YAML)
