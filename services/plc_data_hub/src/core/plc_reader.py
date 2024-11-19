import asyncio
import json

from sqlalchemy.ext.asyncio import AsyncSession

from services.plc_data_hub.src.plc import PLCClient, models
from shared.db.manufactory.models.models import PLCData
from shared.utils.logger import logger

DB_NUMBER = 500


class Reader:
    """Класс для взаимодействия с ПЛК, чтения данных из заданного DB и извлечения информации о типах данных."""

    def __init__(self, ip: str, db_session: AsyncSession):
        if db_session is None:
            raise ValueError("db_session не может быть None")  # Дополнительная проверка
        self.client = PLCClient(ip)
        self.db_session = db_session
        self.data_buffer = []
        self.filled_array = 0
        self.readings = {}
        self.last_readings = {}

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

                # Разбираем прочитанные данные
                self.readings[name] = model.read_func(data, bit_offset)
            else:
                logger.warning(f'Неизвестный тип данных: {data_type}')

    async def save_changes(self):
        """
        Сохраняет изменения в базу данных, если значения отличаются от предыдущих.
        """
        for name, value in self.readings.items():
            if isinstance(value, list):  # Если это список словарей
                current_items = value  # Оставляем как есть, если уже словари
                previous_items = self.last_readings.get(name, [])

                # Сравниваем элементы списка
                for current_item in current_items:
                    if current_item not in previous_items:
                        new_data = PLCData(name=name, value=str(current_item))
                        await new_data.add(self.db_session)

            elif self.last_readings.get(name) != value:  # Если это не список
                new_data = PLCData(name=name, value=str(value))
                await new_data.add(self.db_session)

        # Обновляем last_readings
        self.last_readings = self.readings.copy()

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

                self.read_from_db()
                await self.save_changes()
                await asyncio.sleep(0.1)
