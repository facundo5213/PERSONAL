from models.base import BaseModel
from typing import List, Optional

    
class CategoriesMenuInput(BaseModel):
    name: str
    description: str


class CategoriesMenuComplete(CategoriesMenuInput):
    restaurant_id: str