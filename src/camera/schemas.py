# src/camera/schemas.py

from pydantic import BaseModel, HttpUrl

from src.camera.services import _get_h265

class CameraModel(BaseModel):
    cameraId: int
    cameraURL: HttpUrl
    cameraTimeShift: int
