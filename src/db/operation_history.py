# scr/db/operation_history.py

from sqlalchemy import Column, Text, BigInteger, DateTime
from datetime import datetime

from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Text)
    program = Column(Text)
    data = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)
