from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from utils.presentation.errors import AlreadyExistsException, NotFoundException
from typing import List

from models.final_articles import FinalArticlesModel as modelo_
from repositories.final_articles import FinalArticlesRepository as Repository_
from schemas.final_articles import FinalArticlesInput as Schemas_ , FinalArticlesInputComplet

ITEM = "final_articles"

class FinalArticles:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)
        self.collection = self.main_db["final_articles"]

    #metodo para agregar item
    async def add(self, input: Schemas_, restaurant_id) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")

        """ Validaciones """
        # Valido la existencia de la Category asignada (si no es None)
        if input.category_id != None:
            existing_category = await self.main_db.categories_menu.find_one({"_id": input.category_id})
            if not existing_category:
                raise NotFoundException("Invalid category_id")
        
        # Valido la existencia de las options asignadas
        for option in input.options:
            existing_option = await self.main_db.options.find_one({"_id": option.id})
            if not existing_option:
                raise NotFoundException("Some option's id is invalid")
            
        # Valido la existencia de los components asignados
        for component in input.components:
            existing_component = await self.main_db.components.find_one({"_id": component.id})
            if not existing_component:
                raise NotFoundException("Some component's id is invalid")
            
        # Valido la existencia de los ingredients asignados
        for ingredient in input.ingredients:
            existing_ingredient = await self.main_db.ingredients.find_one({"_id": ingredient.id})
            if not existing_ingredient:
                raise NotFoundException("Some ingredient's id is invalid")
        """ Fin de las validaciones"""
        input_data = input.model_dump()  # Usamos model_dump() aquí en lugar de dict()
        input_data["restaurant_id"] = restaurant_id 
        input_model = FinalArticlesInputComplet.parse_obj(input_data)

        item_db = await self.repository.create(input_model)
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
        
    async def change(self, _id: str, modify_input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Get {ITEM} from db, {ITEM}_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")

        """ Validaciones """
        # Valido la existencia de la Category asignada (si no es None)
        if modify_input.category_id != None:
            existing_category = await self.main_db.categories_menu.find_one({"_id": modify_input.category_id})
            if not existing_category:
                raise NotFoundException("Invalid category_id")
        
        # Valido la existencia de las options asignadas
        for option in modify_input.options:
            existing_option = await self.main_db.options.find_one({"_id": option.id})
            if not existing_option:
                raise NotFoundException("Some option's id is invalid")
            
        # Valido la existencia de los components asignados
        for component in modify_input.components:
            existing_component = await self.main_db.components.find_one({"_id": component.id})
            if not existing_component:
                raise NotFoundException("Some component's id is invalid")
            
        # Valido la existencia de los ingredients asignados
        for ingredient in modify_input.ingredients:
            existing_ingredient = await self.main_db.ingredients.find_one({"_id": ingredient.id})
            if not existing_ingredient:
                raise NotFoundException("Some ingredient's id is invalid")
        """ Fin de las validaciones"""
        
        self.api_response.logger.info(f"Patch {ITEM}_db in db.")
        item_db = await self.repository.patch(_id, modify_input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> None:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        await self.repository.soft_delete(_id)


    # Obtenemos los final_articles pertenecientes a un category_id
    async def get_final_articles_by_category_id(self, category_id: str) -> List[modelo_]:
        final_article_cursor = self.main_db.final_articles.find({"category_id": category_id})  # Consultar por category_id
        final_article_list = await final_article_cursor.to_list(length=None)  # Convertir el cursor a lista
        return final_article_list
    
    async def get_by_ids(self, article_ids: List[str]) -> List[dict]:
        """Obtiene los artículos finales por una lista de IDs."""
        self.api_response.logger.info(f"Fetching articles with IDs: {article_ids}")
        
        # Consulta a la base de datos con múltiples IDs
        articles = await self.collection.find({"_id": {"$in": article_ids}}).to_list(length=None)
        self.api_response.logger.info(f"Fetched articles: {articles}")
        return articles