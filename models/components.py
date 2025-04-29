from models.base import Base
from typing import List, Optional

    
class ComponentsModel(Base):
    _collection_name = "components"
    stock_id: list[dict] = []
    ingredients_id:list[dict] = []
    stock_id: str
    name: str
    description: str
    stock_item_id: str

