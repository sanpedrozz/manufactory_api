from contextlib import asynccontextmanager
from typing import Any, List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        """Автоматически генерировать имя таблицы из имени класса."""
        return self.__name__.lower()

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List[Any]:
        """Получить все записи из таблицы."""
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex

    @classmethod
    async def get_by_id(cls, db: AsyncSession, record_id: int) -> Any:
        """Получить запись по ID."""
        try:
            stmt = select(cls).filter(cls.id == record_id)
            result = await db.execute(stmt)
            instance = result.scalars().first()

            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{cls.__name__} with id {record_id} not found"
                )

            return instance
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex

    @asynccontextmanager
    async def transaction(self, db_session: AsyncSession):
        """Контекстный менеджер для управления транзакциями."""
        try:
            yield
            await db_session.commit()
        except SQLAlchemyError as ex:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex

    async def add(self, db_session: AsyncSession):
        """Добавить запись в базу данных."""
        async with self.transaction(db_session):
            db_session.add(self)

    async def delete(self, db_session: AsyncSession):
        """Удалить запись из базы данных."""
        async with self.transaction(db_session):
            await db_session.delete(self)

    async def update(self, db: AsyncSession, **kwargs):
        """Обновить запись."""
        async with self.transaction(db):
            for k, v in kwargs.items():
                setattr(self, k, v)
