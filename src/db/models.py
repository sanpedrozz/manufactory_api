# src/db/models.py

from sqlalchemy import Column, ForeignKey, Text, Integer, BigInteger, DateTime, JSON, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List, Dict
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
    tag = Column(Text)

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

    @classmethod
    async def get_place_by_id(cls, db: AsyncSession, id: int) -> 'Place':
        try:
            stmt = select(cls).filter(cls.id == id)
            result = await db.execute(stmt)
            place = result.scalars().first()

            if not place:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Place with id {id} not found"
                )

            return place

        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex

    @classmethod
    async def get_cameras_by_place_id(cls, db: AsyncSession, place_id: int) -> List[Dict]:
        """
        Get all camera_info by place_id
        :param db: The database session
        :param place_id: The place ID
        :return: A list of camera_info dictionaries
        """
        try:
            stmt = (
                select(Camera.camera_info)
                .join(PlaceCameraLink, PlaceCameraLink.camera_id == Camera.id)
                .join(cls, PlaceCameraLink.place_id == cls.id)
                .filter(cls.id == place_id)
            )
            result = await db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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


class AlarmMessages(Base):
    __tablename__ = "alarm_messages"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    tag = Column(Text, nullable=True)
    camera = Column(Boolean, default=False, nullable=False)

    @classmethod
    async def get_all(cls, db: AsyncSession) -> List["AlarmMessages"]:
        """
        Get all Alarm
        :param db: The database session
        :return: A list of all Alarm records
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

    @classmethod
    async def get_alarm_by_id(cls, db: AsyncSession, id: int) -> 'AlarmMessages':
        try:
            stmt = select(cls).filter(cls.id == id)
            result = await db.execute(stmt)
            alarm = result.scalars().first()

            if not alarm:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Alarm with id {id} not found"
                )

            return alarm

        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(ex)
            ) from ex
