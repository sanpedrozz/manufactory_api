from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.place.services import get_all_places
from src.database import get_db
from src.db.models import Place
router = APIRouter()


@router.get("/places")
async def get_places(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список устройств (Place) для выпадающего меню.
    """
    return await get_all_places(db)


# @router.post("/save_data")
# async def save_data(data: dict, db: AsyncSession = Depends(get_db)):
#     """
#     Сохраняет данные в таблице OperationHistory.
#     :param data: JSON-объект, содержащий DataBlock и Data.
#     """
#     # Запись данных в БД
#     operation = OperationHistory(
#         place_id=data['place_id'],
#         text=str(data['data_blocks']),  # Преобразуем JSON в строку для хранения
#         program="PLC data"  # Можно добавить описание или название программы
#     )
#     db.add(operation)
#     await db.commit()
#     return {"status": "success"}


@router.post("/save_place_data")
async def save_place_data(place_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    """
    Сохраняет DataBlock и Data в колонке data_config таблицы Place.
    :param place_id: Идентификатор устройства (Place).
    :param data: JSON-объект, содержащий DataBlock и Data.
    """
    place = await db.get(Place, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Сохраняем данные в колонке data_config
    place.data_config = data
    await db.commit()
    return {"status": "success"}
