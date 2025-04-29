from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from utils.presentation.errors import AlreadyExistsException, NotFoundException

from api.final_articles.final_articles_service import FinalArticles
from api.categories_menu.categories_menu_service import CategoriesMenuService
from models.general_menu import GeneralMenuModel as modelo_
from repositories.general_menu import GeneralMenuRepository as Repository_
from schemas.general_menu import GeneralMenuInput as Schemas_ , MenuResponse, GeneralMenuInputComplet


ITEM = "general_menu"

class GeneralMenu:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)

    #metodo para agregar item
    async def add(self, input: Schemas_, restaurant_id) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")

        # Valido la existencia de los final_articles asignados
        if input.final_articles != None:
            for article in input.final_articles:
                existing_article = await self.main_db.final_articles.find_one({"_id": article})
                if not existing_article:
                    raise NotFoundException("Some final_article's id is invalid")
                
        # Valido la existencia de los daily_menu asignados
        if input.daily_menu != None:
            for menu in input.daily_menu:
                existing_menu = await self.main_db.daily_menu.find_one({"_id": menu})
                if not existing_menu:
                    raise NotFoundException("Some daily_menu's id is invalid")
 
        # Agrego restaurant_id al input
        input_data = input.model_dump()  # Usamos model_dump() aquí en lugar de dict()
        input_data["restaurant_id"] = restaurant_id 
        input_model = GeneralMenuInputComplet.model_validate(input_data)
        
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

        # Valido la existencia de los final_articles asignados
        if modify_input.final_articles != None:
            for article in modify_input.final_articles:
                existing_article = await self.main_db.final_articles.find_one({"_id": article})
                if not existing_article:
                    raise NotFoundException("Some final_article's id is invalid")
                
        # Valido la existencia de los final_articles asignados
        if modify_input.daily_menu != None:
            for menu in modify_input.daily_menu:
                existing_menu = await self.main_db.daily_menu.find_one({"_id": menu})
                if not existing_menu:
                    raise NotFoundException("Some daily_menu's id is invalid")
                
        self.api_response.logger.info(f"Patch {ITEM}_db in db.")
        item_db = await self.repository.patch(_id, modify_input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para pasar delete en true
    async def delete_by_id(self,_id:str) -> None:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        await self.repository.soft_delete(_id)



    async def get_menu_with_articles(self, menu_id: str) -> MenuResponse:
        self.api_response.logger.info(f"Init get menu from db, menu_id: {menu_id}")
        
        # Obtener el menú por ID
        menu = await self.repository.get_active_by_id(menu_id)
        if not menu:
            raise NotFoundException("Menu not found")
        
        # Obtener los IDs de los artículos finales
        final_article_ids = menu.final_articles
        
        
        # Servicio para obtener los artículos
        article_service = FinalArticles(self.api_response, self.main_db)

        articles = await article_service.get_by_ids(final_article_ids)
        category_service = CategoriesMenuService(self.api_response, self.main_db)
        
        # Agrupar artículos por categoría
        grouped_articles = {}
        for article in articles:
            category_id = article.get("category_id", "Uncategorized")
            
            # Obtener el objeto de la categoría
            category_obj = await category_service.get_by_id(category_id)
            category_name = category_obj.get("name", "Unknown")
            
            # Usar una clave compuesta (ID y nombre)
            category_key = {"id": category_id, "name": category_name}
            
            # Agrupar los artículos bajo esta categoría
            if category_id not in grouped_articles:
                grouped_articles[category_id] = {
                    "id": category_id,
                    "name": category_name,
                    "articles": []
                }
            
            grouped_articles[category_id]["articles"].append({
                "id": str(article["_id"]),
                "name": article["name"],
                "description": article["description"],
                "options": article["options"],
                "price": article["price"]
            })

        # Formatear la respuesta final
        menu_dict = menu.model_dump()
        menu_dict["final_articles"] = list(grouped_articles.values())
        
        self.api_response.logger.info(f"Finish get menu from db, menu_id: {menu_id}")
        
        return menu_dict