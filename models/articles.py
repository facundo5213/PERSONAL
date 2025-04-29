from models.base import Base
from typing import List, Optional

    
class ArticlesModel(Base):
    _collection_name = "articles"
        
    nombre: str
    unidad: int
    impuesto: float
    merma: float 
    creado: str 
    categoria: str
    descripcion: str
    comentarios: str
    min_stock: int