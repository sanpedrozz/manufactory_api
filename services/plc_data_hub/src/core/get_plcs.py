import asyncio

from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models.models import Place


async def fetch_places():
    """
    Получить список PLC с подходящими именами и IP-адресами.
    :return: Список записей Place с заполненными IP.
    """
    async with AsyncSessionFactory() as session:
        places = await Place.get_all(session)
        return [
            place for place in places
            if place.ip is not None and 'Nanxing 8.' in place.name]


if __name__ == "__main__":
    # Запуск функции
    asyncio.run(fetch_places())
