from shared.db.manufactory.database import AsyncSessionFactory
from shared.db.manufactory.models.models import Place


async def get_filtered_places(session):
    """
    Фильтрует записи Place, которые содержат IP-адрес и определенную подстроку в имени.

    :param session: Сессия базы данных.
    :return: Список объектов Place, соответствующих условиям.
    """
    places = await Place.get_all(session)
    return [place for place in places if place.ip and 'Кромочник' in place.name]


async def fetch_places():
    """
    Получает список PLC с подходящими именами и IP-адресами.

    :return: Список объектов Place.
    """
    async with AsyncSessionFactory() as session:
        return await get_filtered_places(session)
