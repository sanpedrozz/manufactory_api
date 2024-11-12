from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from shared.db.industrial_stg.database import AsyncSessionFactory
from shared.db.industrial_stg.models import Item, IndustryOperationsHistory


# Асинхронная функция для получения данных из базы
# Async function to fetch data from the database
async def get_items_info(label_ids: List[int]):
    async with AsyncSessionFactory() as session:
        items_query = select(Item).where(Item.label_id.in_(label_ids))
        items = (await session.execute(items_query)).scalars().all()

        history_object_ids = [item.history_object_id for item in items if item.history_object_id]
        # Use joinedload to eagerly load the place relationship
        history_query = (
            select(IndustryOperationsHistory)
            .options(joinedload(IndustryOperationsHistory.place))
            .where(IndustryOperationsHistory.object_id.in_(history_object_ids))
        )
        history_results = (await session.execute(history_query)).scalars().all()

        return items, history_results
