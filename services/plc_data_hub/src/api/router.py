from fastapi import FastAPI

router = FastAPI()


@router.get("/data")
async def read_plc_data():
    return {"data": "Data from PL!!!!!!!!!!!!!!!!!!!C"}

@router.get("/")
async def read_plc_data():
    return {"data": "фцвфцвфцвфцв!!!!!!!!!!!!!!C"}
