# src/operation_history/schemas.py

from pydantic import BaseModel
from typing import Optional, Union


class OperationHistory(BaseModel):
    place: Union[str, int]
    program: str
    data: Optional[Union[str, dict]] = None
