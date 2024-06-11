# src/operation_history/schemas.py

from pydantic import BaseModel


class Alarm(BaseModel):
    place_id: int
    alarm: int
