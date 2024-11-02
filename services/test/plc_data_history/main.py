import time

from snap7 import client
from snap7.util import get_string, get_int, get_real, get_bool, get_dint

# Исходные данные
plc_paste = '''
var_String	String	0.0
var_Int	Int	256.0
var_Real	Real	258.0
var_Bool	Bool	262.0
var_DInt	DInt	264.0
'''

client = client.Client()
client.connect('192.168.23.190', 0, 1)


def get_address_by_var(var):
    address = var['address']
    byte, bit = address.split(".")
    return int(byte), int(bit)


def get_var_size_by_var(var):
    var_size = {
        'String': 256,
        'Int': 2,
        'Real': 4,
        'Bool': 1,
        'DInt': 4,
    }
    return var_size.get(var['data_type'])


def get_func_by_data_type(data_type):
    type_to_function = {
        'String': get_string,
        'Int': get_int,
        'Real': get_real,
        'Bool': get_bool,
        'DInt': get_dint,
    }
    return type_to_function.get(data_type)


def get_var_by_string(string):
    var_data = string.split()
    return {'name': var_data[0], 'data_type': var_data[1], 'address': var_data[2]}


def get_strings_by_data(plc_paste):
    values = []
    for var in plc_paste.strip().split('\n'):
        data = get_var_by_string(var)
        value = get_var_value(data)
        values.append({data['name']: value})
    print(values)


def get_var_value(data):
    data_type = data['data_type']
    func = get_func_by_data_type(data_type)
    address = get_address_by_var(data)
    size = get_var_size_by_var(data)

    if data_type == 'Bool':
        value = func(db_data, address[0], address[1])
    else:
        value = func(db_data, address[0])

    return value


if __name__ == '__main__':
    while True:
        # db_data = client.db_read(11, 0, 268)
        # get_strings_by_data(plc_paste)
        # time.sleep(0.1)
        print('OK')