from typing import List

from sqlalchemy.future import select

from shared.db.industrial_stg.database import AsyncSessionFactory
from shared.db.industrial_stg.models import Item, IndustryOperationsHistory


# Асинхронная функция для получения данных из базы
async def get_items_info(label_ids: List[int]):
    async with AsyncSessionFactory() as session:
        items_query = select(Item).where(Item.label_id.in_(label_ids))
        items = (await session.execute(items_query)).scalars().all()

        history_object_ids = [item.history_object_id for item in items if item.history_object_id]
        history_query = select(IndustryOperationsHistory).where(
            IndustryOperationsHistory.object_id.in_(history_object_ids))
        history_results = (await session.execute(history_query)).scalars().all()

        return items, history_results
