from motor.motor_asyncio import AsyncIOMotorDatabase

from models.employee import EmployeeModel
from models.tables import TablesModel

from repositories.employees import EmployeesRepository
from repositories.tables import TableRepository
from schemas.employees import EmployeeInput, EmployeeInputComplete
from utils.presentation.response import ApiResponse

from fastapi import HTTPException

class EmployeesService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.employee_repository = EmployeesRepository(self.main_db)
        self.tables_repository = TableRepository(self.main_db)

    #metodo para agregar empleado
    async def add_employee(self, employee_input: EmployeeInput, restaurant_id) -> EmployeeModel:
        self.api_response.logger.info(f"Create employee in db.")
        #valido que no exista un empleado con el mismo numero
        existing_employee = await self.main_db.employee.find_one({"identifier":employee_input.identifier})
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee already registered")
        
        input_data = employee_input.model_dump()
        input_data["restaurant_id"] = restaurant_id
        input_model = EmployeeInputComplete.parse_obj(input_data)
        
        employee_db = await self.employee_repository.create(input_model)
        self.api_response.logger.info(f"employe_db: {employee_db}")
        return employee_db
    
    #metodo para traer todos los empleados - aun falta el filtro de usuario o restorante
    async def get_employee(self) -> list[EmployeeModel]:
        self.api_response.logger.info("Init get employee from db.")
        employees_db = await self.employee_repository.get_all_actives()
        self.api_response.logger.info(f"employes: {employees_db}")
        return employees_db
    
    async def get_employee_by_identifier(self, employee_identifier: int) -> EmployeeModel:
        self.api_response.logger.info(f"Init get employee from db, employe_id: {employee_identifier}")
        employee_db = await self.employee_repository.get_active_by_identifier(employee_identifier)
        if employee_db:
            self.api_response.logger.info(f"Employee found: {employee_db['identifier']}")
        else:
            self.api_response.logger.info(f"No employee found with identifier: {employee_identifier}")
        return employee_db
    
    #metodo para traer un empleado en particular
    async def get_employee_by_id(self, employee_id: str) -> EmployeeModel:
        self.api_response.logger.info(f"Init get employee from db, employe_id: {employee_id}")
        employee_db = await self.employee_repository.get_active_by_id(employee_id)
        self.api_response.logger.info(f"employee_db: {employee_id}")
        return employee_db
    
    #metodo para cambiar un empleado
    async def change_employee(self, employee_id: str, modify_employee_input: EmployeeInput) -> EmployeeModel:
        self.api_response.logger.info(f"Get employee from db, employee_id: {employee_id}")
        employee_db = await self.employee_repository.get_active_by_id(employee_id)
        self.api_response.logger.info(f"employee_db: {employee_db}")
        self.api_response.logger.info(f"Patch employee_db in db.")
        employee_db = await self.employee_repository.patch(employee_id, modify_employee_input)
        self.api_response.logger.info(f"employee_db: {employee_db}")
        return employee_db
    
    #metodo para pasar delete en true
    async def delete_employee_by_id(self,employee_id:str) -> None:
        self.api_response.logger.info(f"Init delete employee from db, employee_id: {employee_id}")
        employee = await self.employee_repository.soft_delete(employee_id)
        return employee


    #metodo para traer todas las mesass de un empleado:
    async def get_employee_tables(self, employee_id: str) -> list[TablesModel]:
        self.api_response.logger.info(f"Init get tables for employee from db, employee_id: {employee_id}")
        employee_db = await self.employee_repository.get_active_by_id(employee_id)
        
        if not employee_db:
            raise HTTPException(status_code=404, detail="Employee not found")
        cursor = await self.tables_repository.find({"assigned_employee": employee_id})
        tables_db = await cursor.to_list(length=100)
        self.api_response.logger.info(f"Tables for employee_id {employee_id}: {tables_db}")
        return tables_db
    
    async def get_employees_by_restaurant_id(self, restaurant_id: str) -> list[EmployeeModel]:
        employees_cursor = self.main_db.employee.find({"restaurant_id": restaurant_id, "is_deleted": False})  # Consultar por restaurant_id
        employees_list = await employees_cursor.to_list(length=None)  # Convertir el cursor a lista
        return employees_list