from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from src.db.base import Base


class PlaceCameraLink(Base):
    __tablename__ = "place_camera_link"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    place_id = Column(BigInteger, ForeignKey('places.id'), nullable=False)
    camera_id = Column(BigInteger, ForeignKey('cameras.id'), nullable=False)

    place = relationship("Place", back_populates="camera_links")
    camera = relationship("Camera", back_populates="places")
