# src/main.py

from fastapi import FastAPI
from src.operation_history.router import router as operation_history
from src.alarms.router import router as alarms
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Manufactory API", version="1.0.0")

app.include_router(
    operation_history,
    prefix="/operation_history",
    tags=["operation_history"]
)
app.include_router(
    alarms,
    prefix="/alarms",
    tags=["alarms"]
)

app.mount("/static", StaticFiles(directory="src/operation_history/static"), name="static")
