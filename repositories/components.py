from models.components import ComponentsModel
from repositories.crud import BaseRepository


class ComponentsRepository(BaseRepository[ComponentsModel]):
    _entity_model = ComponentsModel
