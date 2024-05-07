# /src/operation_history/services.py

from sqlalchemy.ext.asyncio import AsyncSession
from src.operation_history.schemas import OperationHistory as OperationHistorySchema
from src.db.operation_history import OperationHistory as OperationHistoryDB


async def add_operation_history(db: AsyncSession, operation_history_data: OperationHistorySchema):
    new_operation = OperationHistoryDB(
        place_id=str(operation_history_data.place),
        program=operation_history_data.program,
        data=operation_history_data.data if operation_history_data.data else ""
    )
    await new_operation.save(db)  # Используем метод save из базового класса
    return new_operation
