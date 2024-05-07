# scr/db/operation_history.py

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))  # Используем ForeignKey для связи
    program = Column(Text)
    data = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Places", back_populates="operations")
