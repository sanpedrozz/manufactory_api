import asyncio

from services.plc_data_hub.src.core.get_plcs import fetch_places  # Импорт функции из get_plcs.py
from services.plc_data_hub.src.core.plc_reader import Reader  # Предполагается, что Reader реализован
from shared.db.manufactory.database import AsyncSessionFactory


async def initialize_readers():
    async with AsyncSessionFactory() as session:  # Создаём реальную сессию базы данных
        places = await fetch_places()  # Получаем список PLC

        if not places:
            print("Нет подходящих PLC для подключения.")
            return

        tasks = []

        for place in places:
            print(f"Инициализация Reader для {place.name} ({place.ip})")

            # Передаём реальную сессию
            reader = Reader(ip=place.ip, db_session=session)
            tasks.append(reader.run())

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(initialize_readers())
