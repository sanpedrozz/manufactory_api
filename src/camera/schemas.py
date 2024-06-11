# src/camera/schemas.py

from pydantic import BaseModel, HttpUrl


class CameraModel(BaseModel):
    cameraId: int
    cameraURL: HttpUrl
    cameraTimeShift: int
