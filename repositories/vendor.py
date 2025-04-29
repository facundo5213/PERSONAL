from models.vendor import VendorModel
from repositories.crud import BaseRepository


class VendorRepository(BaseRepository[VendorModel]):
    _entity_model = VendorModel
