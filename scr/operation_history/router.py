# src/operation_history/router.py

from fastapi import APIRouter

from scr.operation_history.schemas import OperationHistory
from scr.operation_history.services import add_operation_history, error_report

router = APIRouter()


@router.post("/add")
def get_work_mode(data: OperationHistory):
    place = data.place
    program = data.program
    data = data.data
    try:
        add_operation_history(place, program, data)
    except:
        error_report()
    return place
