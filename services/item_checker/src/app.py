from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from services.item_checker.src.routers import routers
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Подключаем маршруты
app.include_router(routers.router)

# Подключение статических файлов (для стилей)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="/app/services/item_checker/src/static"), name="static")
