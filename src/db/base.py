from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        """Автоматически генерировать имя таблицы из имени класса."""
        return self.__name__.lower()

    # Добавление экземпляра в базу данных
    async def add(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(ex)
            ) from ex

    # Удаление экземпляра из базы данных
    async def delete(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex)
            ) from ex

    # Обновление полей экземпляра
    async def update(self, db: AsyncSession, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            await db.commit()
        except SQLAlchemyError as ex:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex)
            ) from ex
