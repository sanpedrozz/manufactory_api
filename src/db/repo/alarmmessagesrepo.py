from src.db.repo._base_repo import BaseRepo
from src.db.model.alarmmessages import AlarmMessages

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List


class AlarmMessagesRepo(BaseRepo):
    model = AlarmMessages

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List[model]:
        """
        Get all AlarmMessages records.
        :param db: The database session.
        :return: A list of all AlarmMessages records.
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

    @classmethod
    async def get_alarm_by_id(cls, db: AsyncSession, alarm_id: int) -> AlarmMessages:
        """
        Get an AlarmMessages record by ID.
        :param db: The database session.
        :param alarm_id: The alarm ID.
        :return: The AlarmMessages record.
        """
        try:
            stmt = select(cls.model).filter(cls.model.id == alarm_id)
            result = await db.execute(stmt)
            alarm = result.scalars().first()

            if not alarm:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Alarm with id {alarm_id} not found"
                )

            return alarm
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex
