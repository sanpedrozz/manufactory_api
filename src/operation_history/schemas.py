# src/operation_history/schemas.py

from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class OperationHistory(BaseModel):
    place: int
    program: str
    data: Optional[Union[str, dict]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OperationList(BaseModel):
    TotalRecords: int
    RecordsFiltered: int
    operations: list[OperationHistory]

    class Config:
        from_attributes = True
