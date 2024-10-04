from pydantic import BaseModel
from typing import Optional, Union


class OperationHistory(BaseModel):
    place: int
    program: str
    data: Optional[Union[str, dict]] = None

    class Config:
        from_attributes = True


class OperationList(BaseModel):
    TotalRecords: int
    RecordsFiltered: int
    operations: list[OperationHistory]

    class Config:
        from_attributes = True
