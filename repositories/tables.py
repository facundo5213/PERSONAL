from models.tables import TablesModel
from repositories.crud import BaseRepository


class TableRepository(BaseRepository[TablesModel]):
    _entity_model = TablesModel

    async def find(self, filter: dict):
        cursor = self.collection.find(filter)
        return cursor
