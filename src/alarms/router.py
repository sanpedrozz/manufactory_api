# src/alarms/router.py

from fastapi import APIRouter
from src.alarms.schemas import Alarm
from src.alarms.services import send_message
router = APIRouter()


@router.post("/alarm")
async def read_alarm(alarm: Alarm):
    await send_message(alarm)
    return alarm
