import asyncio

from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models.models import Place


async def fetch_places():
    # Открываем сессию для базы данных
    async with AsyncSessionFactory() as session:
        # Получаем все записи из таблицы Place
        places = await Place.get_all(session)
        for place in places:
            if place.ip is not None and place.name == "Nanxing 8.2 (Кромочник)":
                print(place.ip)


# Запуск функции
asyncio.run(fetch_places())
