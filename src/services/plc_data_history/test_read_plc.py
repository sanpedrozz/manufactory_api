from src.services.plc_data_history.models import models, PLC
from src.services.plc_data_history.plc_client import PLCClient

plc_data = '''
YEAR	UInt	0.0
MONTH	USInt	2.0
DAY	USInt	3.0
WEEKDAY	USInt	4.0
HOUR	USInt	5.0
MINUTE	USInt	6.0
SECOND	USInt	7.0

'''

def parse_address(address):
    try:
        byte, bit = address.split(".")
        return int(byte), int(bit)
    except ValueError:
        raise ValueError(f"Некорректный адрес: {address}")

def parse_var_description(line):
    var_data = line.split()
    return {'name': var_data[0], 'data_type': var_data[1], 'address': var_data[2]}

def read_var_value(db_data, var):
    byte, bit = parse_address(var['address'])
    data_type_model = models.get(var['data_type'])

    if var['data_type'] == 'Bool':
        return data_type_model.read_func(db_data, byte, bit)
    else:
        return data_type_model.read_func(db_data, byte)

def validate_var(var):
    if len(var.split()) != 3:
        raise ValueError(f"Некорректная строка переменной: {var}. Ожидается формат 'имя тип адрес'.")

    name, data_type, address = var.split()

    if data_type not in models:
        raise ValueError(f"Некорректный тип данных: {data_type}. Допустимые типы: {list(models.keys())}.")
    try:
        if data_type == 'Bool':
            byte, bit = address.split(".")
            if not (byte.isdigit() and bit.isdigit()):
                raise ValueError
        else:
            byte, bit = address.split(".")
            if not byte.isdigit():
                raise ValueError
    except ValueError:
        raise ValueError(f"Некорректный адрес: {address} для типа {data_type}.")

def get_var_values(db_data, plc_paste):
    variables = []
    for line in plc_paste.strip().split('\n'):
        print(line)
        validate_var(line)  # Проверяем корректность строки
        var = parse_var_description(line)
        value = read_var_value(db_data, var)
        variables.append({var['name']: value})
    return variables


plc_client = PLCClient(PLC(ip = '192.168.23.31', name='KDT1'))

db_data = plc_client.read_data(49, 24, 14)
values = get_var_values(db_data, plc_data)
print(values)
#
# db_data = client.db_read(49, 24, 14)  # Чтение данных DB 11
# values = get_var_values(db_data, plc_paste)
# print(values)
