# scr/db/places.py

from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship
from src.db.base import Base


class Places(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    comment = Column(Text)

    # Опционально: обратная связь с OperationHistory
    operations = relationship("OperationHistory", back_populates="place")
