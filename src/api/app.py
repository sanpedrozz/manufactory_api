from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.alarm.router import router as alarms
from src.api.operation.router import router as operation
from src.api.place.router import router as place

app = FastAPI(title="Manufactory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Если хочешь ограничить домены, можно указать конкретные.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    alarms,
    prefix="/alarms",
    tags=["Аварии"]
)

app.include_router(
    operation,
    prefix="/operation",
    tags=["Операции"]
)

app.include_router(
    place,
    prefix="/place",
    tags=["Устройства"]
)