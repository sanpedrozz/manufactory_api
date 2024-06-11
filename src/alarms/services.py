# src/alarms/services.py

import logging
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.db.models import Camera, Place, PlaceCameraLink
from src.camera.services import get_video
from src.alarms.schemas import Alarm
from src.database import get_db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def send_message(alarm: Alarm, db: AsyncSession = Depends(get_db)):
    smth = get_camera_info_by_place_id(db, alarm.place_id)
    print(smth)


async def get_camera_info_by_place_id(db: AsyncSession, place_id: int):
    try:
        # Select the place and join the necessary relationships
        stmt = select(Place).options(
            joinedload(Place.camera_links).joinedload(PlaceCameraLink.camera)
        ).filter(Place.id == place_id)

        result = await db.execute(stmt)
        place = result.scalars().first()

        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Place with id {place_id} not found"
            )

        # Extract camera_info from the linked cameras
        camera_info_list = [link.camera.camera_info for link in place.camera_links]
        return camera_info_list

    except SQLAlchemyError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        ) from ex
