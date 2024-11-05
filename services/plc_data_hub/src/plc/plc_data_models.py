from snap7.util import get_string, get_int, get_real, get_bool, get_dint, get_uint, get_usint


class DataType:
    """Базовый класс для типов данных ПЛК."""

    def __init__(self, name, size, read_func):
        self.name = name
        self._size = size
        self.read_func = read_func

    @property
    def size(self):
        """Возвращает размер типа данных в байтах."""
        return self._size


class StringDataType(DataType):
    """Тип данных String с определённым размером, использует get_string из snap7."""

    def __init__(self, size=256):
        super().__init__(f"String[{size}]", size + 2 if size <= 254 else size, get_string)


class IntDataType(DataType):
    """Целочисленный тип данных, использует get_int из snap7."""

    def __init__(self):
        super().__init__('Int', 2, get_int)


class RealDataType(DataType):
    """Тип данных Real (с плавающей точкой), использует get_real из snap7."""

    def __init__(self):
        super().__init__('Real', 4, get_real)


class BoolDataType(DataType):
    """Булевый тип данных, использует get_bool из snap7."""

    def __init__(self):
        super().__init__('Bool', 1, get_bool)


class UIntDataType(DataType):
    """Тип данных беззнаковое целое, использует get_uint из snap7."""

    def __init__(self):
        super().__init__('UInt', 2, get_uint)


class USIntDataType(DataType):
    """Тип данных беззнаковое малое целое, использует get_usint из snap7."""

    def __init__(self):
        super().__init__('USInt', 1, get_usint)


class DIntDataType(DataType):
    """Тип данных двойное целое, использует get_dint из snap7."""

    def __init__(self):
        super().__init__('DInt', 4, get_dint)


# Соответствие типов данных моделям
models: dict[str, DataType] = {
    f'String[{i}]': StringDataType(i) for i in range(1, 255)
}

# Добавляем остальные типы данных
models.update({
    'String': StringDataType(),
    'Int': IntDataType(),
    'Real': RealDataType(),
    'Bool': BoolDataType(),
    'UInt': UIntDataType(),
    'USInt': USIntDataType(),
    'DInt': DIntDataType(),
})
