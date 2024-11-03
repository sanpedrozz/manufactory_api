import asyncio
import snap7
from shared.utils.logger import logger


class PLCReader:
    def __init__(self):
        self.client = snap7.client.Client()
        self.data_buffer = []

    def connect(self):
        try:
            self.client.connect('192.168.23.190', 0, 1)
            logger.info("Connected to PLC")
        except Exception as e:
            logger.error(f"PLC connection error: {e}")

    async def run(self):
        self.connect()
        while True:
            try:
                data = self.client.db_read(100, 0, 10)  # Чтение блока данных
                self.data_buffer.append(data)
                print(data)
                await asyncio.sleep(1)  # Интервал чтения
            except Exception as e:
                logger.error(f"Error reading data: {e}")


if __name__ == "__main__":
    plc = PLCReader()
    asyncio.run(plc.run())

