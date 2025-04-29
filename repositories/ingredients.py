from models.ingredients import IngredientsModel
from repositories.crud import BaseRepository


class IngredientsRepository(BaseRepository[IngredientsModel]):
    _entity_model = IngredientsModel
