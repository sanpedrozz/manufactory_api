# src/operation_history/router.py

from fastapi import APIRouter

from src.operation_history.schemas import OperationHistory
from src.operation_history.services import add_operation_history, error_report
from src.utils.logging import AppLogger
from src.db.base import Base
from src.database import get_db

from datetime import datetime

logger = AppLogger().get_logger()

router = APIRouter()


@router.post("/add")
async def get_work_mode(data: OperationHistory):
    with get_db() as session:
        time = datetime.now()
        place = data.place
        program = data.program
        data = data.data
        try:
            items = add_operation_history(time, place, program, data)
            Base.update(session, items)
        except:
            items = error_report(time)
            Base.update(session, items)
    return place
