from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.db.models import Place

router = APIRouter()


@router.get("/places")
async def get_places(db: AsyncSession = Depends(get_db)):
    return await Place.get_all(db)
