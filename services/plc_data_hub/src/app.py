from fastapi import FastAPI

from src.api.router import router

app = FastAPI(root_path="/plc-data", title="PLC API", version="1.0.0")

# Подключение API
app.include_router(router.router)
