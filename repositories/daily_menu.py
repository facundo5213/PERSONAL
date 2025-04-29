from models.daily_menu import Daily_MenuModel
from repositories.crud import BaseRepository


class Daily_MenuRepository(BaseRepository[Daily_MenuModel]):
    _entity_model = Daily_MenuModel
