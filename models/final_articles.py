from models.base import Base
from typing import List, Optional
    
class FinalArticlesModel(Base):
    _collection_name = "final_articles"
    
    category_id : Optional[str] = None
    restaurant_id: str
    kitchen : str
    name : str
    description : str
    price : float
    is_prepared : bool
    options : List[dict] = []
    components : List[dict] = []
    ingredients : List[dict] = []
    stock_controlled : bool