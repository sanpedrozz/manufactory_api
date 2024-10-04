from fastapi import FastAPI
from src.api.alarm.router import router as alarms
from src.api.operation_history.router import router as operation_history

app = FastAPI(title="Manufactory API", version="1.0.0")

app.include_router(
    alarms,
    prefix="/alarms",
    tags=["Аварии"]
)

app.include_router(
    operation_history,
    prefix="/operation_history",
    tags=["operation_history"]
)
