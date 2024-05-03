from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    Integer,
    BigInteger,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


from scr.db.base import Base

class OperationHistory(Base):
    __tablename__ = "operations_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    place_id: Mapped[str] = mapped_column(String)
    dt: Mapped