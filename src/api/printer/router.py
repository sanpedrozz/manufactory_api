import random

from fastapi import APIRouter, HTTPException

from src.api.printer.schemas import LabelRequest
from src.api.printer.services import print_label_service

router = APIRouter()

# Инициализируем начальные значения
x_value = 100
y_value = 100
x_max = 2700
y_max = 1900


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
    global x_value, y_value

    data = {
        "id": random.randint(100000000000000, 999999999999999),
        "x": x_value,
        "y": y_value,
        "a": random.choice([False, True]),
    }

    # Обновляем координаты для следующего вызова
    x_value += 100
    if x_value > x_max:
        x_value = 100
        y_value += 100
        if y_value > y_max:
            y_value = 100  # Сбрасываем y после достижения максимума

    # 10% шанс вернуть {"result": "done"}
    if random.random() < 0.1:
        return {"result": "done"}

    return data


@router.post("/print", name="print_label")
async def print_label(label_request: LabelRequest):
    try:
        await print_label_service(label_request.label_id)
        return {"status": "Printed successfully"}
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail="Printer connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
