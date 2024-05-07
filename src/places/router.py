from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.operation_history.schemas import OperationHistory
from src.operation_history.services import add_operation_history
from src.database import get_db

router = APIRouter()


@router.post("/add")
async def add_operation_history_endpoint(operation_history_data: OperationHistory, db: AsyncSession = Depends(get_db)):
    try:
        operation = await add_operation_history(db, operation_history_data)
        return {"message": "Operation history added successfully", "operation_id": operation.id}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/update")
async def update_operation_history_endpoint(operation_history_data: OperationHistory,
                                            db: AsyncSession = Depends(get_db)):
    try:
        operation = await add_operation_history(db, operation_history_data)
        return {"message": "Operation history added successfully", "operation_id": operation.id}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
