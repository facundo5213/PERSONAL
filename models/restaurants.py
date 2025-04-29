from models.base import Base
from typing import List, Optional



class RestaurantsModel(Base):
    _collection_name = "restaurants"

    name: str
    phone: str
    address: str
    comments: str
    #employees: List[dict] = []



class RestaurantsModelResponseId(Base):
    _collection_name = "restaurants"

    name: str
    phone: str
    address: str
    comments: str
    #employees: List[dict] = []
    rooms: List[dict] = []