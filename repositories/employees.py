from models.employee import EmployeeModel
from repositories.crud import BaseRepository
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

class EmployeesRepository(BaseRepository[EmployeeModel]):
    _entity_model = EmployeeModel

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.get_collection(self._entity_model._collection_name.default)
        

    async def get_active_by_identifier(self, employee_identifier: int) -> EmployeeModel:
        return await self.collection.find_one({"identifier": employee_identifier})
    

    