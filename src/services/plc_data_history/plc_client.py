from functools import wraps
from time import sleep

from snap7 import client

from src.services.plc_data_history.models import PLC


def reconnect_on_fail(reconnect_delay=5):
    """
    Декоратор для автоматического переподключения к PLC при сбоях подключения.
    :param reconnect_delay: Задержка (в секундах) между попытками переподключения.
    :return: Декорированная функция.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            while True:
                try:
                    if self.connected:
                        return function(self, *args, **kwargs)
                    self.connect()
                except OSError as error:
                    self.disconnect()
                    sleep(reconnect_delay)
        return wrapper
    return decorator


class PLCClient:
    def __init__(self, plc: PLC):
        """
        Инициализация клиента для подключения к PLC.
        :param plc: PLC
        """
        self.ip = plc.ip
        self.client = client.Client()
        self.connect()

    @property
    def connected(self):
        """
        Проверка, установлено ли подключение с контроллером PLC.
        :return: True, если соединение установлено, иначе False
        """
        return self.client.get_connected()

    def connect(self):
        """
        Установить подключение с контроллером PLC.
        """
        try:
            self.client.connect(self.ip, 0, 1)
        except Exception as e:
            raise RuntimeError(f"Ошибка подключения к PLC по адресу {self.ip}") from e

    def disconnect(self):
        """
        Разорвать подключение с контроллером PLC.
        """
        try:
            self.client.disconnect()
        except Exception as e:
            raise RuntimeError(f"Ошибка отключения от PLC {self.ip}") from e

    @reconnect_on_fail()
    def read_data(self, db: int, offset: int, size: int):
        """
        Чтение данных из указанной области памяти (DB) контроллера PLC.
        :param db: Номер области памяти (DB).
        :param offset: Смещение начального байта в области памяти.
        :param size: Размер читаемых данных (в байтах).
        :return: Прочитанные данные
        """
        try:
            return self.client.db_read(db, offset, size)
        except Exception as e:
            raise RuntimeError(f"Ошибка чтения данных с PLC {self.ip}") from e

    @reconnect_on_fail()
    def write_data(self, db: int, start: int, data: bytearray):
        """
        Запись данных в указанную область памяти (DB) контроллера PLC.
        :param db: Номер области памяти (DB).
        :param start: Смещение начального байта в области памяти.
        :param data: Данные для записи в байтах.
        """
        try:
            self.client.db_write(db, start, data)
        except Exception as e:
            raise RuntimeError(f"Ошибка записи данных в PLC {self.ip}") from e
