from models.base import Base
from typing import List, Optional

class IngredientsModel(Base):
    _collection_name = "ingredients"

    name: str
    description: str
    restaurant_id :str
    min_stock: int
