from sqlalchemy import Column, Text, BigInteger, JSON
from sqlalchemy.orm import relationship

from src.db.base import Base


class Camera(Base):
    __tablename__ = "cameras"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    camera_info = Column(JSON)
    comment = Column(Text)

    places = relationship("PlaceCameraLink", back_populates="camera")
