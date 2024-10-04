from typing import Optional, Union

from pydantic import BaseModel


class OperationHistory(BaseModel):
    place: int
    program: str
    data: Optional[Union[str, dict]] = None

    class Config:
        from_attributes = True
