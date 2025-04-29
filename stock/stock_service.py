import asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from models.stock import StockModel as modelo_
from models.orders import OrdersModel as order
from repositories.stock import StockRepository as Repository_
from schemas.stock import StockInput as Schemas_

ITEM = "stock"

class StockService:
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
    
    async def order_substraction(self,final_article_list: list[dict], options_list: list[dict], session):
        update_queries = []
        for article in final_article_list:
            update_queries.append(
                UpdateOne(
                    {"_id": article["id"]},
                    {"$inc": {"quantity": -article["quantity"]}}
                )
            )
        for option in options_list:
            update_queries.append(
                UpdateOne(
                    {"_id": option["id"]},
                    {"$inc": {"quantity": -option["quantity"]}}
                )
            )
        await asyncio.sleep(600)
        if update_queries:
            await self.stock_repository.bulk_update(update_queries, session=session)    
    
    
    async def change(self, _id: str, modify_input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Get {ITEM} from db, {ITEM}_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        self.api_response.logger.info(f"Patch {ITEM}_db in db.")
        item_db = await self.repository.patch(_id, modify_input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> None:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        await self.repository.soft_delete(_id)