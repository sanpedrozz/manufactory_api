# src/operation_history/schemas.py

from pydantic import BaseModel
from typing import Optional, Union


class OperationHistory(BaseModel):
    place: int
    program: str
    data: Optional[Union[str, dict]] = None

    class Config:
        from_attributes = True
