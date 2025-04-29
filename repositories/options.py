from models.options import OptionsModel
from repositories.crud import BaseRepository


class OptionsRepository(BaseRepository[OptionsModel]):
    _entity_model = OptionsModel
