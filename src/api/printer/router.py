import random

from fastapi import APIRouter, HTTPException

from src.api.printer.schemas import LabelRequest
from src.api.printer.services import print_label_service

router = APIRouter()

# Начальные значения
initial_id = 100001000000000
current_id = initial_id
x_value = 150
y_value = 150
x_min, x_max = 150, 2650
y_min, y_max = 150, 350
a_value = False
toggle_counter = 0  # Счётчик для переключения


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
    global current_id, x_value, y_value, a_value, toggle_counter

    # Формируем данные
    data = {
        "id": current_id,
        "x": x_value,
        "y": y_value,
        "a": a_value,
    }

    # Обновляем id
    current_id += 1000000000

    # Обновляем координаты
    x_value += 100
    if x_value > x_max:
        x_value = x_min
        y_value += 100
        if y_value > y_max:
            # Сброс значений после достижения максимальных
            x_value = x_min
            y_value = y_min
            current_id = initial_id
            return {"result": "done"}

    # Меняем значение каждые 5 запросов
    toggle_counter += 1
    if toggle_counter >= 5:
        a_value = not a_value
        toggle_counter = 0

    return data


@router.get("/reset", name="reset_coordinates")
async def reset_coordinates():
    global current_id, x_value, y_value, a_value, toggle_counter

    # Сброс всех значений
    current_id = initial_id
    x_value = x_min
    y_value = y_min
    a_value = False
    toggle_counter = 0

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
