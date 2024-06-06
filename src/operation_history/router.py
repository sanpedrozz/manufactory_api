# src/operation_history/router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.operation_history.schemas import OperationHistory
from src.operation_history.services import (add_operation_history,
                                            get_all_operations)
from src.database import get_db

from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post("/add", name="add_operation_history")
async def add_operation_history_endpoint(operation_history_data: OperationHistory, db: AsyncSession = Depends(get_db)):
    try:
        operation = await add_operation_history(db, operation_history_data)
        return {"message": "Operation history added successfully", "operation_id": operation.id}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/list", name="list_operation_histories")
async def get_operation_history_list(
        db: AsyncSession = Depends(get_db),
        limit: int = Query(100, title="Limit", description="Limit the number of returned logs", ge=1)
):
    try:
        operations = await get_all_operations(db, limit=limit)
        return operations
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/", response_class=HTMLResponse)
async def get_index():
    with open("src/operation_history/static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
