from models.base import Base
from typing import List
    
class StockModel(Base):
    _collection_name = "stock"
    
    restaurant_id: str
    ingredient_id: str
    quantity: str 
    unit: float
    minimum_threshold: int 
    last_updated: str 
    min_stock: int 
    unit_price: float
    vendor: List[str]
    