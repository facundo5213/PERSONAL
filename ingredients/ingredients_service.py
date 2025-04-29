from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from utils.presentation.errors import AlreadyExistsException, NotFoundException
from models.ingredients import IngredientsModel as modelo_
from repositories.ingredients import IngredientsRepository as Repository_
from schemas.ingredients import IngredientsInput as Schemas_ , IngredientsComplete
from typing import List

ITEM = "ingredients"

class IngredientsService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)

    #metodo para agregar item
    async def add(self, input: Schemas_, restaurant_id) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")

        input_data = input.model_dump()  # Usamos model_dump() aquí en lugar de dict()
        input_data["restaurant_id"] = restaurant_id
        input_model = IngredientsComplete.parse_obj(input_data)

        item_db = await self.repository.create(input_model)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para traer todos los ingredients
    async def get(self) -> list[modelo_]:
        self.api_response.logger.info("Init get {ITEM} from db.")
        item_db = await self.repository.get_all_actives()
        self.api_response.logger.info(f"employes: {item_db}")
        return item_db
    
    #metodo para traer un ingredient en particular
    async def get_by_id(self, _id: str) -> modelo_:
        self.api_response.logger.info(f"Init get {ITEM} from db, ingredient_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {_id}")
        return item_db


    #metodo para cambiar un empleado
    async def change(self, _id: str, modify_input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Get {ITEM} from db, {ITEM}_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        self.api_response.logger.info(f"Patch {ITEM}_db in db.")
        item_db = await self.repository.patch(_id, modify_input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> modelo_:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        await self.repository.soft_delete(_id)
        
        