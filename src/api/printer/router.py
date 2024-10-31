import random

from fastapi import APIRouter, HTTPException

from src.api.printer.schemas import LabelRequest
from src.api.printer.services import print_label_service

router = APIRouter()

# Начальные значения
coords_counter = 0  # Счётчик для переключения
coords = [{'x': 200, 'y': 200, "a": False},
          {'x': 2500, 'y': 200, "a": False},
          {'x': 2500, 'y': 1800, "a": True},
          {'x': 200, 'y': 1800, "a": True}]


@router.get("/get_data", name="get_print_params")
async def get_printer_params():
    data = {
        "id": random.randint(100000000000000, 999999999999999),
        "x": random.randint(100, 2700),
        "y": random.randint(100, 1900),
        "a": random.choice([False, True]),
    }

    # 10% шанс вернуть {"result": "done"}
    if random.random() < 0.1:
        return {"result": "done"}

    return data


@router.get("/get_data_test", name="get_data_test")
async def get_data_test():
    global coords, coords_counter

    # Формируем данные
    data = {
        "id": random.randint(100000000000000, 999999999999999),
        "x": coords[coords_counter]["x"],
        "y": coords[coords_counter]["y"],
        "a": coords[coords_counter]["a"],
        "coords_counter": coords_counter
    }

    # Обновляем координаты
    coords_counter += 1
    if coords_counter >= 4:
        coords_counter = 0
        return {"result": "done"}

    return data


@router.get("/reset", name="reset_coordinates")
async def reset_coordinates():
    global coords_counter

    # Сброс всех значений
    coords_counter = 0

    return {"status": "reset done"}


@router.post("/print", name="print_label")
async def print_label(label_request: LabelRequest):
    try:
        await print_label_service(label_request.label_id)
        return {"status": "Printed successfully"}
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail="Printer connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
