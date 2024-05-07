# scr/main.py

from fastapi import FastAPI
from src.operation_history.router import router as operation_history
from src.places.router import router as places

app = FastAPI(title="Manufactory API", version="0.2.0")

app.include_router(
    operation_history,
    prefix="/operation_history",
    tags=["operation_history"]
)
app.include_router(
    places,
    prefix="/places",
    tags=["places"]
)

