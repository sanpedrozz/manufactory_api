import re

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.item_checker.src.util.main import get_items_info

router = APIRouter()
templates = Jinja2Templates(directory="/app/services/item_checker/src/templates")


# Маршрут для отображения HTML-страницы с формой и таблицей
@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# Маршрут для обработки данных формы и отображения таблицы
@router.post("/view", response_class=HTMLResponse)
async def display_table(request: Request, label_input: str = Form(...)):
    # Process input data to extract label IDs
    label_ids = list(map(int, re.findall(r'\d+', label_input)))

    # Get items and history results including place name
    items, history_results = await get_items_info(label_ids)

    # Prepare operation facts with place name and creation time
    operation_facts = {}
    for record in history_results:
        place_name = record.place.name if record.place else "Неизвестное место"
        creation_time = record.creation_dt.strftime('%Y-%m-%d %H:%M:%S')

        fact_description = ""
        if record.operation_id == 17 and record.operation_property1:
            if record.operation_property1 in [1, 2]:
                fact_description = f"L{record.operation_property1}"
            elif record.operation_property1 in [3, 4]:
                fact_description = f"W{record.operation_property1}"
        elif record.operation_id == 18:
            fact_description = "ПРИСАДКА"

        if fact_description:
            # Add fact with time and place name
            operation_facts.setdefault(record.object_id, []).append(
                f"{fact_description} (Время: {creation_time}, Место: {place_name})"
            )

    # Prepare data for table
    table_data = []
    for item in items:
        edges = [
            f"L1: {item.edge_length_1}" if item.edge_length_1 else "",
            f"L2: {item.edge_length_2}" if item.edge_length_2 else "",
            f"W3: {item.edge_width_3}" if item.edge_width_3 else "",
            f"W4: {item.edge_width_4}" if item.edge_width_4 else ""
        ]
        edge_info = ", ".join(filter(None, edges)) or "Нет"
        is_preassembled = 'Да' if item.plan_set_id and '18' in item.plan_set_id else 'Нет'

        operation_fact = "<br>".join(
            operation_facts.get(item.history_object_id, ["Нет операции"])) or "Нет операции"

        table_data.append({
            "label_id": item.label_id,
            "history_object_id": item.history_object_id,
            "is_preassembled": is_preassembled,
            "edge_info": edge_info,
            "operation_fact": operation_fact
        })

    return templates.TemplateResponse("table.html", {"request": request, "table_data": table_data})
