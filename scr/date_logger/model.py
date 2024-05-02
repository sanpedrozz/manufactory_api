#   scr/data_logger/model.py

from pydantic import BaseModel
from typing import Optional, Union


class WorkMode(BaseModel):
    place: Union[str, int]
    program: str
    data: Optional[Union[str, dict]] = None
