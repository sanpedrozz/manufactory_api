from typing import Optional
from pydantic import BaseModel


class Alarm(BaseModel):
    place_id: int
    alarm: int
    details: Optional[str] = None
