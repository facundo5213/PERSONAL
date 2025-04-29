from models.base import Base
from typing import List, Optional

class CategoriesMenuModel(Base):
    _collection_name = "categories_menu"

    # menu_id: str
    name: str
    description: str
    restaurant_id: str

class CategoriesMenuModelResponseId(Base):
    _collection_name = "categories_menu"

    # menu_id: str
    name: str
    description: str
    restaurant_id: str
    final_articles: List[dict] = []