from sqlalchemy import Column, Text, BigInteger, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from datetime import datetime


class OperationHistory(Base):
    __tablename__ = "operations_history"

    id = Column(BigInteger, primary_key=True)
    place_id = Column(Text)
    program = Column(Text)
    data = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    # async def add_operation(self, db_session: AsyncSession):
