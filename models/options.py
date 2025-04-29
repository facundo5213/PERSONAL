from models.base import Base
from typing import List, Optional

    
class OptionsModel(Base):
    _collection_name = "options"
        
    name: str
    description: str
    type : str
    component: List[dict] = []
    ingredient: List[dict] = []
    price_modifier : float






    