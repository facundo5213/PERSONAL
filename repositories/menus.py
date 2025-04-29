from models.menus import MenusModel
from repositories.crud import BaseRepository


class MenuRepository(BaseRepository[MenusModel]):
    _entity_model = MenusModel
