#   /scr/data_logger/model.py

from pydantic import BaseModel


class WorkMode(BaseModel):
    place: str
    program: str
    data: str | None | dict
