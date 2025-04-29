from models.general_menu import GeneralMenuModel
from repositories.crud import BaseRepository


class GeneralMenuRepository(BaseRepository[GeneralMenuModel]):
    _entity_model = GeneralMenuModel
