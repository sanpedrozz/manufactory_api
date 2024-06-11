# src/alarms/router.py

from fastapi import APIRouter
from src.alarms.schemas import Alarm

router = APIRouter()


@router.post("/alarm")
async def read_alarm(alarm: Alarm):
    return alarm
