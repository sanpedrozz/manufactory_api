# scr/db/places.py

from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import relationship

from src.db.base import Base


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)
    comment = Column(Text)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)
