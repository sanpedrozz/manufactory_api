from pydantic import BaseModel


class DataItem(BaseModel):
    type: str
    address: str


class DataBlock(BaseModel):
    data_block: int
    data: dict[str, DataItem]
