# src/operation_history/services.py

import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.operation_history.schemas import OperationHistory as OperationHistorySchema
from src.db.model.operationhistory import OperationHistory as OperationHistoryDB
from src.db.repo.operationhistoryrepo import OperationHistoryRepo
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from sqlalchemy.sql.expression import func

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def add_operation_history(db: AsyncSession, operation_history_data: OperationHistorySchema):
    new_operation = OperationHistoryDB(
        place_id=operation_history_data.place,
        program=operation_history_data.program,
        text=operation_history_data.data if operation_history_data.data else "",
        dt_created=datetime.now(),
    )
    await new_operation.add(db)
    return new_operation


async def get_all_operations(db: AsyncSession, limit: int = 100) -> List[OperationHistorySchema]:
    try:
        repo = OperationHistoryRepo()
        # result = await db.execute(select(OperationHistoryDB).order_by(desc(OperationHistoryDB.dt_created)).limit(limit))
        # operations = result.scalars().all()
        ans = [
            OperationHistorySchema(
                place=op.place_id,
                program=op.program,
                data=op.text,
                created_at=op.dt_created,
            ) for op in await OperationHistoryRepo.get_all(db, limit=limit)
        ]
        logger.info(ans)
        return ans
    except SQLAlchemyError as ex:
        logger.error(f"Database error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {ex}")
    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {ex}")


async def get_operation_part(db: AsyncSession, page: int = 1, limit: int = 25) -> List[OperationHistorySchema]:
    try:
        result = await db.execute(
            select(OperationHistoryDB).order_by(desc(OperationHistoryDB.dt_created)).offset((page - 1) * limit).limit(
                limit))
        total_count = await db.execute(select(func.count()).select_from(OperationHistoryDB))
        total_count = total_count.scalars().all()[0]
        operations = result.scalars().all()
        response = [
            OperationHistorySchema(
                place=op.place_id,
                program=op.program,
                data=op.text,
                created_at=op.dt_created,
            ) for op in operations
        ]
        return response, len(response), total_count
    except SQLAlchemyError as ex:
        logger.error(f"Database error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {ex}")
    except Exception as ex:
        logger.error(f"Unexpected error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {ex}")
