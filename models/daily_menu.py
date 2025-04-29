from models.base import Base
from typing import List, Optional
    
class Daily_MenuModel(Base):
    _collection_name = "daily_menu"
    
    restaurant_id: str
    date: str
    item: List[dict] = [] 
    special_price: float
    
    