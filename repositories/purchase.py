from models.purchase import PurchaseModel
from repositories.crud import BaseRepository


class PurchaseRepository(BaseRepository[PurchaseModel]):
    _entity_model = PurchaseModel
 