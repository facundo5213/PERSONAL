from models.final_articles import FinalArticlesModel
from repositories.crud import BaseRepository


class FinalArticlesRepository(BaseRepository[FinalArticlesModel]):
    _entity_model = FinalArticlesModel
