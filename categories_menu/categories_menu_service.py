from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from ..final_articles.final_articles_service import FinalArticles

from models.categories_menu import CategoriesMenuModel as modelo_, CategoriesMenuModelResponseId
from repositories.categories_menu import CategoriesMenuRepository as Repository_
from schemas.categories_menu import CategoriesMenuInput as Schemas_, CategoriesMenuComplete

from utils.presentation.response import ApiResponse
from utils.presentation.errors import AlreadyExistsException, NotFoundException

ITEM = "categories_menu"

class CategoriesMenuService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)

    #metodo para agregar item
    async def add(self, input: Schemas_, restaurant_id) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")

        # # Valido la existencia del general_menu asignado
        # existing_general_menu = await self.main_db.general_menu.find_one({"_id": input.menu_id})
        # if not existing_general_menu:
        #     raise NotFoundException("Invalid menu_id")

        # # Valido la existencia de esa Room en el Restaurant asignado
        # existing_room = await self.main_db.rooms.find_one({"room_number": input.room_number, "restaurant_id": input.restaurant_id})
        # if existing_room:
        #     raise AlreadyExistsException("Room already registered in that restaurant")
        
        # Creamos el ingredient en el repositorio correspondiente

        input_data = input.model_dump()  # Usamos model_dump() aquí en lugar de dict()  
        input_data["restaurant_id"] = restaurant_id
        input_model= CategoriesMenuComplete.model_validate(input_data)

        item_db = await self.repository.create(input_model)
        
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para traer todos los categories_menu
    async def get(self) -> list[modelo_]:
        self.api_response.logger.info("Init get {ITEM} from db.")
        item_db = await self.repository.get_all_actives()
        self.api_response.logger.info(f"employes: {item_db}")
        return item_db
    
    #metodo para traer un categories_menu en particular
    async def get_by_id(self, _id: str) -> CategoriesMenuModelResponseId:
        self.api_response.logger.info(f"Init get {ITEM} from db, categories_menu_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {_id}")
        final_article_service = FinalArticles(self.api_response, self.main_db) 
        final_articles_db = await final_article_service.get_final_articles_by_category_id(_id)
        item_db_dict = item_db.model_dump()  
        item_db_dict["final_articles"] = final_articles_db
        self.api_response.logger.info(f"{ITEM}_db: {_id}")
        return item_db_dict


    #metodo para cambiar un categories_menu
    async def change(self, _id: str, modify_input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Get {ITEM} from db, {ITEM}_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")

        # # Valido la existencia del general_menu asignado
        # existing_general_menu = await self.main_db.general_menu.find_one({"_id": modify_input.menu_id})
        # if not existing_general_menu:
        #     raise NotFoundException("Invalid menu_id")
        
        self.api_response.logger.info(f"Patch {ITEM}_db in db.")
        item_db = await self.repository.patch(_id, modify_input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> modelo_:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        
        # Verificamos que no hayan Final Articles pertenecientes a la Category
        final_articles_service = FinalArticles(self.api_response, self.main_db) 
        final_articles_db = await final_articles_service.get_final_articles_by_category_id(_id)
        if final_articles_db:
            raise AlreadyExistsException("The Category has active Final Articles")

        instance = await self.repository.soft_delete(_id)
        print(instance)
        return instance