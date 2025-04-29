from models.base import BaseModel
from typing import List, Optional

class Daily_MenuInput(BaseModel):
    restaurant_id: str
    date: str
    item: List[dict] = [] 
    special_price: float
