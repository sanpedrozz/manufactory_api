from fastapi import FastAPI
from src.api.alarm.router import router as alarms
from src.api.operation_history.router import router as operation_history
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "operation_history/static", html=True),
          name="static")
