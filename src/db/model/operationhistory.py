from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    program = Column(Integer)
    text = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Place", back_populates="operations")
