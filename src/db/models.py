# src/db/models.py

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime, JSON
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List
from datetime import datetime

from src.db.base import Base


class OperationHistory(Base):
    __tablename__ = "operations_history"
    id = Column(BigInteger, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    program = Column(Text)
    text = Column(Text)
    dt_created = Column(DateTime, default=datetime.now)

    place = relationship("Place", back_populates="operations")

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["OperationHistory"]:
        """
        Get all OperationHistory records
        :param db: The database session
        :return: A list of all OperationHistory records
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex


class Place(Base):
    __tablename__ = "places"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text)

    operations = relationship("OperationHistory", back_populates="place", post_update=True)
    camera_links = relationship("PlaceCameraLink", back_populates="place")

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["Place"]:
        """
        Get all Place records
        :param db: The database session
        :return: A list of all Place records
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex


class Camera(Base):
    __tablename__ = "cameras"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    camera_info = Column(JSON)
    comment = Column(Text)

    places = relationship("PlaceCameraLink", back_populates="camera")

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["Camera"]:
        """
        Get all Camera records
        :param db: The database session
        :return: A list of all Camera records
        """
        try:
            stmt = select(cls)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex)
            ) from ex


class PlaceCameraLink(Base):
    __tablename__ = "place_camera_link"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    place_id = Column(BigInteger, ForeignKey('places.id'), nullable=False)
    camera_id = Column(BigInteger, ForeignKey('cameras.id'), nullable=False)

    place = relationship("Place", back_populates="camera_links")
    camera = relationship("Camera", back_populates="places")
