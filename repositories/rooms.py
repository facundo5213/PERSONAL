from models.rooms import RoomsModel
from repositories.crud import BaseRepository


class RoomsRepository(BaseRepository[RoomsModel]):
    _entity_model = RoomsModel
