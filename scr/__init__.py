#   scr/__init__.py

from fastapi import FastAPI
from scr.date_logger.router import date_logger

app = FastAPI()
app.include_router(date_logger, prefix="/logs")
