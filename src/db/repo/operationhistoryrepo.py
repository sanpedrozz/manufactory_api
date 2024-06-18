from src.db.repo._base_repo import BaseRepo
from src.db.model.operationhistory import OperationHistory

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime, JSON, Boolean, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List, Dict
from datetime import datetime
from typing import TypeVar, List


class OperationHistoryRepo(BaseRepo):
    model = OperationHistory

    @classmethod
    async def get_all(cls, db: AsyncSession, limit: int | None = None) -> List[model]:
        """
        Get all records.
        :param db: The database session.
        :return: A list of all records.
        """
        try:
            if limit:
                stmt = select(cls.model).limit(limit)
            else:
                stmt = select(cls.model)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex