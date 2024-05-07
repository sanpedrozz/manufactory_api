# src/operation_history/base.py

from typing import Any
from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        """Automatically generate the table name from the class name."""
        return self.__name__.lower()

    async def add(self, db_session: AsyncSession):
        """
        Add the current instance to the database
        :param db_session:
        :return:
        """
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(ex)
            ) from ex

    async def delete(self, db_session: AsyncSession):
        """
        Delete the current instance from the database
        :param db_session:
        :return:
        """
        try:
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex)
            ) from ex

    async def update(self, db: AsyncSession, **kwargs):
        """
        Update fields of the current instance
        :param db:
        :param kwargs
        :return:
        """
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

    async def add_or_update(self, db: AsyncSession):
        """
        Save or update the current instance depending on its state in the database.
        :param db:
        :return:
        """
        try:
            db.add(self)
            await db.commit()
        except IntegrityError as exception:
            await db.rollback()
            if isinstance(exception.orig, UniqueViolationError):
                await db.merge(self)
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=repr(exception),
                ) from exception
        finally:
            await db.close()
