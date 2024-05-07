# scr/db/models.py

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    program = Column(Text)
    data = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Place", back_populates="operations")


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    comment = Column(Text)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)
