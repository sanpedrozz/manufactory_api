# src/alarms/router.py

from fastapi import APIRouter, Depends
from src.alarms.schemas import Alarm
from src.alarms.services import send_message

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

router = APIRouter()


@router.post("/alarm")
async def read_alarm(alarm: Alarm, db: AsyncSession = Depends(get_db)):
    await send_message(db, alarm)
    return alarm
