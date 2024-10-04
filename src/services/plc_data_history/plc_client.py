import traceback
from functools import wraps
from time import sleep

from snap7 import client
from snap7.exceptions import Snap7Exception

from logs.logger import logger


def singleton(cls):
    """
    Декоратор, превращающий класс в синглтон. Обеспечивает, что только один экземпляр класса будет создан.
    :param cls: Класс, который нужно превратить в сингл тон
    :return: Превращенный в синглтон класс
    """
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


def reconnect_on_fail(max_retries=3600, delay=5):
    """
    Декоратор, обеспечивающий повторное подключение к контроллеру PLC при сбоях соединения.
    :param max_retries: Максимальное количество попыток подключения
    :param delay: Задержка (в секундах) между попытками переподключения
    :return: Декорированная функция
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    if self.connected:
                        return function(self, *args, **kwargs)
                    self.connect()
                except Exception as error:
                    logger.warning(f'PLC error for {self.ip}: {error}:\n\n {traceback.format_exc()}\n')
                    self.disconnect()
                    sleep(delay)
                    retries += 1
            raise Snap7Exception(f'Не удалось выполнить функцию после {max_retries} повторных попыток')
        return wrapper
    return decorator


@singleton
class PLCClient:
    def __init__(self, ip: str):
        self.ip = ip
        self.client = client.Client()
        self.connect()

    @property
    def connected(self):
        """
        Проверяет, установлено ли соединение с контроллером PLC
        :return: True, если соединение установлено, иначе False
        """
        return self.client.get_connected()

    def connect(self):
        """
        Устанавливает соединение с контроллером PLC.
        """
        return self.client.connect(self.ip, 0, 1)

    def disconnect(self):
        """
        Разрывает соединение с контроллером PLC.
        """
        return self.client.disconnect()

    @reconnect_on_fail()
    def read_data(self, db_number: int, offset: int, size: int):
        """
        Читает данные из указанной области данных (DB) контроллера PLC
        :param db_number: Int - Номер области данных (DB).
        :param offset: Int - Смещение начального байта в области данных.
        :param size: Int - Размер читаемых данных (в байтах).
        :return: Прочитанные данные
        """
        return self.client.db_read(db_number, offset, size)

    @reconnect_on_fail()
    def write_data(self, db_number: int, start: int, data: bytearray):
        """
        Записывает данные в указанную область данных (DB) контроллера PLC
        :param db_number: Int - Номер области данных (DB).
        :param start: Int - Смещение начального байта в области данных.
        :param data: Int - Размер читаемых данных (в байтах).
        :return: Результат операции записи (количество записанных байт).
        """
        return self.client.db_write(db_number, start, data)
