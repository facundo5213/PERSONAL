from models.base import Base
from typing import List, Optional

    
class MenusModel(Base):
    _collection_name = "menus"
    
    nombre: str
    descripcion: str
    precio: float