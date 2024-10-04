from snap7.util import get_string, get_int, get_real, get_bool, get_dint, get_uint, get_usint


class DataType:
    def __init__(self, name, size, read_func):
        self.name = name
        self.size = size
        self.read_func = read_func


class StringDataType(DataType):
    def __init__(self):
        super().__init__('String', 256, get_string)


class IntDataType(DataType):
    def __init__(self):
        super().__init__('Int', 2, get_int)


class RealDataType(DataType):
    def __init__(self):
        super().__init__('Real', 4, get_real)


class BoolDataType(DataType):
    def __init__(self):
        super().__init__('Bool', 1, get_bool)


class UIntDataType(DataType):
    def __init__(self):
        super().__init__('UInt', 2, get_uint)


class USIntDataType(DataType):
    def __init__(self):
        super().__init__('USInt', 1, get_usint)


class DIntDataType(DataType):
    def __init__(self):
        super().__init__('DInt', 4, get_dint)


# Соответствие типов данных моделям
models = {
    'String': StringDataType(),
    'Int': IntDataType(),
    'Real': RealDataType(),
    'Bool': BoolDataType(),
    'UInt': UIntDataType(),
    'USInt': USIntDataType(),
    'DInt': DIntDataType(),
}
