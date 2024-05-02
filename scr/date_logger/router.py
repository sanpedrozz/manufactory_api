#   scr/data_logger/router.py

from fastapi import APIRouter

from scr.date_logger.model import WorkMode
from scr.date_logger.service import get_data, error_report

date_logger = APIRouter()


@date_logger.post("/work_mode")
def get_work_mode(work_mode: WorkMode):
    place = work_mode.place
    program = work_mode.program
    data = work_mode.data
    try:
        get_data(place, program, data)
    except:
        error_report()
    return place
