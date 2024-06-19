from src.db.repo._base_repo import BaseRepo
from src.db.model.camera import Camera

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List


class CameraRepo(BaseRepo):
    model = Camera

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List[model]:
        """
        Get all Camera records.
        :param db: The database session.
        :return: A list of all Camera records.
        """
        try:
            stmt = select(cls.model)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex
