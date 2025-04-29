from models.base import Base

from typing import List, Optional, Literal

class TablesModel(Base):
    _collection_name = "tables"

    table_number: str
    capacity: int
    currently_seated: int
    #is_fusion: bool
    #original_tables_id: List[str] = []
    status: Literal["free", "occupied", "blocked"] = "free"
    orders: List[dict] = [] 
    assigned_employee : str
    room_id: str
    # assigned_at: str # Lo maneja TableAssistment
    x : float
    y : float
    type : Literal["table_circle_small", 
                   "table_circle", 
                   "table_rectangle",
                   "table_small",
                   "table_oval_xl",
                   "table_oval_s",
                   ]
