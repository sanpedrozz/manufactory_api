# /src/operation_history/services.py
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.operation_history.schemas import OperationHistory as OperationHistorySchema
from src.db.models import OperationHistory as OperationHistoryDB
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def add_operation_history(db: AsyncSession, operation_history_data: OperationHistorySchema):
    new_operation = OperationHistoryDB(
        place_id=operation_history_data.place,
        program=operation_history_data.program,
        data=operation_history_data.data if operation_history_data.data else ""
    )
    await new_operation.add(db)
    return new_operation


async def get_all_operations(db: AsyncSession, limit: int = 100) -> List[OperationHistorySchema]:
    try:
        result = await db.execute(select(OperationHistoryDB).order_by(desc(OperationHistoryDB.dt_created)).limit(limit))
        operations = result.scalars().all()
        return [
            OperationHistorySchema(
                place=op.place_id,
                program=op.program,
                data=op.data
            ) for op in operations
        ]
    except SQLAlchemyError as ex:
        logger.error(f"Database error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {ex}")
    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {ex}")
