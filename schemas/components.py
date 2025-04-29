from models.base import BaseModel
from typing import List, Optional

class ComponentsInput(BaseModel):
    stock_id: list[dict] = []
    ingredients_id:list[dict] = []
    name: str
    unit: int
    category: str
    description: str


