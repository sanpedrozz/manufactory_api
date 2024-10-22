from typing import Optional, Dict

from pydantic import BaseModel


class PrintData(BaseModel):
    label_id: int
    length: float
    width: float
    thickness: float
    cover: str
    size: str
    count: str
    order: str
    client_pos: str
    site: str
    comment_lines: list
    comment: str
    l1: Dict[str, Optional[float]]
    l2: Dict[str, Optional[float]]
    w3: Dict[str, Optional[float]]
    w4: Dict[str, Optional[float]]
    l1_other_color: str
    l2_other_color: str
    w3_other_color: str
    w4_other_color: str
    curve: int
    edge_dop: str
    texture: str
    operations_info: str


class LabelRequest(BaseModel):
    label_id: int
