from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.response import ApiResponse
from utils.presentation.errors import AlreadyExistsException
from ..rooms.rooms_service import RoomsService
from ..employees.employees_service import EmployeesService

from models.restaurants import RestaurantsModel as modelo_ , RestaurantsModelResponseId
from repositories.restaurants import RestaurantRepository as Repository_
from schemas.restaurants import RestaurantInput as Schemas_

ITEM = "restaurants"

class RestaurantsService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = Repository_(self.main_db)

    #metodo para agregar item
    async def add(self, input: Schemas_) -> modelo_:
        self.api_response.logger.info(f"Create {ITEM} in db.")

        # Valido la existencia de esa Room
        existing_restaurant = await self.main_db.restaurants.find_one({"name": input.name})
        if existing_restaurant:
            raise AlreadyExistsException("Restaurant already registered")
                
        item_db = await self.repository.create(input)
        self.api_response.logger.info(f"{ITEM}_db: {item_db}")
        return item_db
    
    #metodo para traer todos los restaurant - aun falta el filtro de usuario o restaurant
    async def get(self) -> list[modelo_]:
        self.api_response.logger.info("Init get {ITEM} from db.")
        item_db = await self.repository.get_all_actives()
        self.api_response.logger.info(f"employes: {item_db}")
        return item_db
    
    #metodo para traer un empleado en particular
    async def get_by_id(self, _id: str) -> RestaurantsModelResponseId:
        self.api_response.logger.info(f"Init get {ITEM} from db, employe_id: {_id}")
        item_db = await self.repository.get_active_by_id(_id)
        rooms_service = RoomsService(self.api_response, self.main_db) 
        rooms_db = await rooms_service.get_rooms_by_restaurant_id(_id)
        item_db_dict = item_db.model_dump()  
        item_db_dict["rooms"] = rooms_db

        self.api_response.logger.info(f"{ITEM}_db: {_id}")
        return item_db_dict
    
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
    async def delete_by_id(self,_id:str) -> None:
        self.api_response.logger.info(f"Init delete {ITEM} from db, {ITEM}_id: {_id}")
        
        # Verificamos que no hayan Rooms pertenecientes al Restaurant
        rooms_service = RoomsService(self.api_response, self.main_db) 
        rooms_db = await rooms_service.get_rooms_by_restaurant_id(_id)
        if rooms_db:
            raise AlreadyExistsException("The Restaurant has active Rooms")
        
        # Verificamos que no hayan Employees pertenecientes al Restaurant
        employees_service = EmployeesService(self.api_response, self.main_db) 
        employees_db = await employees_service.get_employees_by_restaurant_id(_id)
        if employees_db:
            raise AlreadyExistsException("The Restaurant has active Employees")

        instance = await self.repository.soft_delete(_id)
        print(instance)
        return instance