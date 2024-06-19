from src.db.repo._base_repo import BaseRepo
from src.db.model.program import Program

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List


class ProgramRepo(BaseRepo):
    model = Program

    @classmethod
    async def get_or_add(cls, db: AsyncSession, name: str) -> int:
        try:
            stmt = select(cls.model).filter(cls.model.program == name)
            result = await db.execute(stmt)
            program = result.scalars().first()
            if not program:
                program = Program(program=name)
                await db.flush()
                await db.refresh(program)
            return program.id

        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex
