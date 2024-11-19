import asyncio

from services.plc_data_hub.src.plc import PLCClient, models

DB_NUMBER = 500


class ItemSendReader:
    """Класс для взаимодействия с ПЛК, чтения данных из заданного DB и извлечения информации о типах данных."""

    def __init__(self, ip: str):
        """Инициализация клиента PLC и создание буфера данных."""
        self.client = PLCClient(ip)
        self.data_buffer = []
        self.filled_array = 0
        self.readings = []  # Список для хранения значений в формате {name: value}

    def _get_filled_array(self):
        """
        Чтение количества заполненных элементов массива из PLC.
        :return: Количество заполненных элементов.
        """
        data = self.client.read_data(db_number=DB_NUMBER, offset=0, size=2)
        return models['UInt'].read_func(data, 0)

    def _get_array(self, filled_array):
        """
        Чтение данных массива из PLC и преобразует их в список словарей.
        :param filled_array: Количество элементов, которые нужно прочитать.
        :return: Список словарей с информацией о каждом элементе массива.
        """
        data_list = []  # Создаем список для хранения всех словарей данных
        # Чтение всех данных одним запросом, если возможно
        for i in range(filled_array):
            data = self.client.read_data(db_number=DB_NUMBER, offset=2 + 60 * i, size=60)
            data_dict = {
                'name': models['String[20]'].read_func(data, 0),
                'type': models['String[30]'].read_func(data, 22),
                'db': models['UInt'].read_func(data, 54),
                'byte': models['UInt'].read_func(data, 56),
                'bit': models['USInt'].read_func(data, 58)
            }
            data_list.append(data_dict)
        return data_list

    def read_from_db(self):
        """
        Чтение данных из другого DB на основе информации из data_buffer.
        :return: Список словарей со значениями в формате {name: value}.
        """
        self.readings.clear()  # Очищаем предыдущие значения
        for entry in self.data_buffer:
            name = entry['name']
            db_number = entry['db']
            byte_offset = entry['byte']
            bit_offset = entry['bit']
            data_type = entry['type']

            # Определяем модель на основе типа данных
            model = models.get(data_type)
            if model:
                # Читаем данные из указанного DB, используя смещение в байтах и бите
                data = self.client.read_data(db_number=db_number, offset=byte_offset, size=model.size)

                # Применяем функцию чтения из модели
                value = model.read_func(data, bit_offset)
                self.readings.append({name: value})  # Добавляем в список словарь {name: value}
            else:
                print(f"Неизвестный тип данных: {data_type}")

        return self.readings  # Возвращаем список значений

    async def run(self):
        """
        Основной цикл чтения данных из PLC.
        """
        with self.client:
            prev_filled_array = None

            while True:
                # Получаем текущее значение filled_array только один раз за цикл
                current_filled_array = self._get_filled_array()
                # Проверяем, изменилось ли значение filled_array
                if current_filled_array != prev_filled_array:
                    # Обновляем данные в буфере только если количество заполненных элементов изменилось
                    self.data_buffer = self._get_array(current_filled_array)
                    prev_filled_array = current_filled_array

                read_from_db = self.read_from_db()
                print(read_from_db)
                # logger.warning(f'{read_from_db}')
                await asyncio.sleep(0.1)


# Запускаем читатель PLC
reader = ItemSendReader('192.168.23.190')
asyncio.run(reader.run())
