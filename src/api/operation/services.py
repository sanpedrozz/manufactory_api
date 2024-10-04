from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.operation.schemas import OperationHistory as OperationHistorySchema
from src.db.models import OperationHistory as OperationHistoryDB


async def add_operation_history(db: AsyncSession, operation_history_data: OperationHistorySchema):
    new_operation = OperationHistoryDB(
        place_id=operation_history_data.place,
        program=operation_history_data.program,
        text=operation_history_data.data if operation_history_data.data else "",
        dt_created=datetime.now(),
    )
    await new_operation.add(db)
