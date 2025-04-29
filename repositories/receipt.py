from models.receipt import ReceiptModel
from repositories.crud import BaseRepository


class ReceiptRepository(BaseRepository[ReceiptModel]):
    _entity_model = ReceiptModel
