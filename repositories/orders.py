from models.orders import OrdersModel
from repositories.crud import BaseRepository


class OrdersRepository(BaseRepository[OrdersModel]):
    _entity_model = OrdersModel
