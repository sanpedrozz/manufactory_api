import random

from fastapi import APIRouter, HTTPException

from src.api.printer.services import print_label_service

router = APIRouter()


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


@router.post("/print", name="print_label")
async def print_label():
    try:
        await print_label_service()
        return {"status": "Printed successfully"}
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail="Printer connection error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
