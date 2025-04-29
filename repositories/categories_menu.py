from models.categories_menu import CategoriesMenuModel
from repositories.crud import BaseRepository


class CategoriesMenuRepository(BaseRepository[CategoriesMenuModel]):
    _entity_model = CategoriesMenuModel
