
from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db

from api.employees.employees_service import EmployeesService

from models.employee import EmployeeModel, EmployeeIdResponse
from models.users import UserResponseModel
from models.tables import TablesModel

from schemas.employees import EmployeeInput, EmployeeLogin
from schemas.response import ResponseBase

from utils.presentation.errors import NotFoundException
from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse
from utils.oauth.auth import get_user_current




employees_router: APIRouter = APIRouter(prefix="/v1/employees")

@employees_router.post(
    "",
    tags=["Employees"],
    summary="Crear un nuevo empleado",
    description="Endpoint para crear un nuevo empleado en el sistema.",
    response_description="El empleado creado.",
)
@response_handler(response_status=status.HTTP_201_CREATED)
async def create_employees(
        request: Request,
        response: Response,
        employee_input: EmployeeInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[EmployeeModel]:
    api_response.logger.info("Init create employee")
    employee_service = EmployeesService(api_response, main_db) ##
    employee = await employee_service.add_employee(employee_input, token.restaurantes) ##
    api_response.logger.info(f"Finish create employee: {employee}") ##
    return employee

@employees_router.post(
    "/login",
    tags=["Employees"],
    summary="Iniciar sesión de empleado",
    description="Endpoint para que un empleado inicie sesión en el sistema. devuelve el id del empleado para ser almacenado en el front. solamente enviar el identificador del empleado.",
    response_description="El ID del empleado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def login_employees(
        request: Request,
        response: Response,
        employee_input: EmployeeLogin,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current)
) -> ResponseBase[EmployeeIdResponse]:
    employee_identifier = employee_input.identifier
    api_response.logger.info("Init get employee")
    employee_service = EmployeesService(api_response, main_db)
    employee = await employee_service.get_employee_by_identifier(employee_identifier)
    if not employee:
        api_response.logger.error(f"Employee identifier '{employee_identifier}' does not exist")
        raise NotFoundException("Employee identifier does not exist")  # Lanzar excepción personalizada
    
    api_response.logger.info(f"Finish get employee: {employee}")
    return EmployeeIdResponse(employee_id=str(employee['_id']))


@employees_router.get(
    "",
    tags=["Employees"],
    summary="Obtener todos los empleados",
    description="Endpoint para obtener todos los empleados del sistema.",
    response_description="Una lista de empleados.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_employees(
    request:Request,
    response:Response,
    api_response=Depends(ApiResponse),
    main_db=Depends(get_mongo_db),
    token: str = Depends(get_user_current)
) -> ResponseBase[list[EmployeeModel]]:
    api_response.logger.info("Init get all employee")
    employee_service = EmployeesService(api_response, main_db)
    employees = await employee_service.get_employee()
    api_response.logger.info(f"Finish get employee: {employees}")
    return employees


@employees_router.get(
    "/{employee_id}",
    tags=["Employees"],
    summary="Obtener empleado por ID",
    description="Endpoint para obtener un empleado por su ID.",
    response_description="El empleado con el ID especificado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_employee(
        request: Request,
        response: Response,
        employee_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current)
) -> ResponseBase[EmployeeModel]:
    api_response.logger.info("Init get employee")
    employee_service = EmployeesService(api_response, main_db)
    employee = await employee_service.get_employee_by_id(employee_id)
    api_response.logger.info(f"Finish get employee: {employee}")
    return employee

@employees_router.patch(
    "/{employee_id}",
    tags=["Employees"],
    summary="Modificar empleado por ID",
    description="Endpoint para modificar un empleado por su ID.",
    response_description="El empleado modificado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_employees(
        request: Request,
        response: Response,
        employee_id: str,
        modify_employee_input: EmployeeInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current)
) -> ResponseBase[EmployeeModel]:
    api_response.logger.info("Init modify employee")
    employee_service = EmployeesService(api_response, main_db)
    employee = await employee_service.change_employee(employee_id, modify_employee_input)
    api_response.logger.info(f"Finish modify employee: {employee}")
    return employee



@employees_router.delete(
    "/{employee_id}",
    tags=["Employees"],
    summary="Eliminar empleado por ID",
    description="Endpoint para eliminar un empleado por su ID.",
    response_description="El empleado eliminado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_employee(
        request: Request,
        response: Response,
        employee_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current)
) -> ResponseBase[EmployeeModel]:
    api_response.logger.info("Init delete employee")
    employee_service = EmployeesService(api_response, main_db)
    employee = await employee_service.delete_employee_by_id(employee_id)
    api_response.logger.info(f"Finish delete employee: {employee}")
    return employee



@employees_router.get(
    "/{employee_id}/tables",
    tags=["Employees"],
    summary="Obtener todas las mesas asignadas a un empleado específico",
    description="Endpoint para obtener todas las mesas asignadas a un empleado específico.",
    response_description="Una lista de mesas asignadas al empleado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_employee_tables(
        request: Request,
        response: Response,
        employee_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current)
) -> ResponseBase[list[TablesModel]]:
    api_response.logger.info(f"Init get tables for employee with ID: {employee_id}")
    employee_service = EmployeesService(api_response, main_db)
    tables = await employee_service.get_employee_tables(employee_id)
    api_response.logger.info(f"Finish get tables for employee: {tables}")
    return tables