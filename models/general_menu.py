from models.base import Base
from typing import List, Optional

    
class GeneralMenuModel(Base):
    _collection_name = "general_menu"
        
    restaurant_id :str
    name :str
    description:str
    final_articles : List[str] = []
    daily_menu : List[str] = []

