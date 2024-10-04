from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.operation.schemas import OperationHistory
from src.api.operation.services import add_operation_history
from src.database import get_db

router = APIRouter()


@router.post("/add", name="add_operation_history")
async def add_operation_history_endpoint(operation_history_data: OperationHistory, db: AsyncSession = Depends(get_db)):
    try:
        await add_operation_history(db, operation_history_data)
        return operation_history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
