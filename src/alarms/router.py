# src/alarms/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.alarms.schemas import Alarm
from src.alarms.services import alarm_message_send
from src.database import get_db

router = APIRouter()


@router.post("/send_alarm")
async def send_alarm(alarm: Alarm, db: AsyncSession = Depends(get_db)):
    await alarm_message_send(db, alarm)
    return alarm
