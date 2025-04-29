import asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from models.purchase import PurchaseModel as modelo_
from repositories.purchase import PurchaseRepository as Repository_
from schemas.purchase import PurchaseInput as Schemas_

ITEM = "purchase"

class PurchaseService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)

    #metodo para agregar item
    async def add(self, input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")
        item_db = await self.repository.create(input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    async def get(self) -> list[modelo_]:
        self.api_response.logger.info("Init get {ITEM} from db.")
        item_db = await self.repository.get_all_actives()
        self.api_response.logger.info(f"employes: {item_db}")
        return item_db
        
    async def get_by_id(self, _id: str) -> modelo_:
        self.api_response.logger.info(f"Init get {ITEM} from db, employe_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {_id}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> None:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        await self.repository.soft_delete(_id)