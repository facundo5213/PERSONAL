from models.base import Base
from typing import List


class OrderHistoryModel(Base):
    _collection_name = "order_history"

    restaurant_id: str
    order_id: str  # ID de la orden modificada
    history: List[dict]  # Lista de los cambios realizados en la orden

