from models.stock import StockModel
from repositories.crud import BaseRepository


class StockRepository(BaseRepository[StockModel]):
    _entity_model = StockModel
