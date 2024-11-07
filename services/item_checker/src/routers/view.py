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
    # Обработка входных данных: удаление пробелов и запятых
    label_ids = list(map(int, re.findall(r'\d+', label_input)))

    items, history_results = await get_items_info(label_ids)

    # Создаем операции для каждого объекта
    operation_facts = {record.object_id: [] for record in history_results}
    for record in history_results:
        if record.operation_id == 17 and record.operation_property1:
            if record.operation_property1 in [1, 2]:
                operation_facts[record.object_id].append(f"L{record.operation_property1}")
            elif record.operation_property1 in [3, 4]:
                operation_facts[record.object_id].append(f"W{record.operation_property1}")
        elif record.operation_id == 18:
            operation_facts[record.object_id].append("ПРИСАДКА")

    # Формируем данные для таблицы
    table_data = []
    for item in items:
        edges = [
            f"L1: {item.edge_length_1}" if item.edge_length_1 else "",
            f"L2: {item.edge_length_2}" if item.edge_length_2 else "",
            f"W1: {item.edge_width_3}" if item.edge_width_3 else "",
            f"W2: {item.edge_width_4}" if item.edge_width_4 else ""
        ]
        edge_info = ", ".join(filter(None, edges)) or "Нет данных о кромке"
        is_preassembled = 'да' if item.plan_set_id and '18' in item.plan_set_id else 'нет'
        operation_fact = "; ".join(
            operation_facts.get(item.history_object_id, ["Нет операции"])).strip() or "Нет операции"

        table_data.append({
            "label_id": item.label_id,
            "is_preassembled": is_preassembled,
            "edge_info": edge_info,
            "operation_fact": operation_fact
        })
    return templates.TemplateResponse("table.html", {"request": request, "table_data": table_data})
