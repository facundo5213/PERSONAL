from models.base import Base

from typing import List, Optional

class RoomsModel(Base):
    _collection_name = "rooms"

    room_number: int  
    description: str
    #tables: List[dict] = [] 
    restaurant_id: str




class RoomsModelResponseId(Base):
    _collection_name = "rooms"

    room_number: int  
    description: str
    #tables: List[dict] = [] 
    restaurant_id: str
    tables: List[dict] = []