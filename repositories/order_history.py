from models.order_history import OrderHistoryModel
from repositories.crud import BaseRepository


class OrderHistoryRepository(BaseRepository[OrderHistoryModel]):
    _entity_model = OrderHistoryModel
