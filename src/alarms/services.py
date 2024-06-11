# src/alarms/services.py

import logging
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from src.db.models import Camera, Place, PlaceCameraLink
from src.camera.services import get_video
from src.alarms.schemas import Alarm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def send_message(db: AsyncSession, alarm: Alarm):
    path_list = []

    cameras_list = await get_camera_info_by_place_id(db, alarm.place_id)
    current_time = datetime.now()

    for camera in cameras_list:
        path_list.append(await get_video(camera, current_time))
        logging.info(f"!!!!!!!!!!!!!!!!!!!!!!! {path_list}")


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

        camera_info_list = [link.camera.camera_info for link in place.camera_links]
        return camera_info_list

    except SQLAlchemyError as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        ) from ex
