from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.place.schemas import DataBlock
from src.database import get_db
from src.db.models import Place

router = APIRouter()


@router.get("/places")
async def get_places(db: AsyncSession = Depends(get_db)):
    return await Place.get_all(db)


@router.post("/places/{place_id}/update_data_for_read")
async def update_data_for_read(place_id: int, data_for_read: list[DataBlock], db: AsyncSession = Depends(get_db)):
    place = await Place.get_place_by_id(db, place_id)
    data_for_read_json = [block.dict() for block in data_for_read]

    if not place:
        raise HTTPException(status_code=404, detail=f"Place with id {place_id} not found")


    await place.update_data_for_read(db, data_for_read_json)
    return {"message": "Data updated successfully"}
