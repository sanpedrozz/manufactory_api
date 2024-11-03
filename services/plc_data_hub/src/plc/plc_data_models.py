from snap7.util import get_string, get_int, get_real, get_bool, get_dint, get_uint, get_usint


class DataType:
    def __init__(self, name, size, read_func):
        self.name = name
        self._size = size
        self.read_func = read_func

    @property
    def size(self):
        return self._size


class StringDataType(DataType):
    def __init__(self, size=256):
        super().__init__(f"String[{size}]", size, get_string)


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
models: dict[str, DataType] = {
    f'String[{i}]': StringDataType(i) for i in range(1, 257)
}

# Добавляем остальные типы данных
models.update({
    'Int': IntDataType(),
    'Real': RealDataType(),
    'Bool': BoolDataType(),
    'UInt': UIntDataType(),
    'USInt': USIntDataType(),
    'DInt': DIntDataType(),
})

if __name__ == '__main__':
    for model_name, model_instance in models.items():
        print(f"{model_name}: Size = {model_instance.size}")
