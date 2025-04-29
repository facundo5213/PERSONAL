from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db

from api.general_menu.general_menu_service import GeneralMenu as Service
from models.general_menu import GeneralMenuModel as Model
from models.users import UserResponseModel

from schemas.general_menu import GeneralMenuInput as Input , MenuResponse
from schemas.response import ResponseBase


from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse
from utils.oauth.auth import get_user_current


ITEM = "general_menu" 

##################################################################################################

general_menu_router: APIRouter = APIRouter(prefix="/v1/general_menu")

@general_menu_router.post(
    "",
    tags=["General Menu"],
    description=f"Create {ITEM}"
)
@response_handler(response_status=status.HTTP_201_CREATED)
async def create(
        request: Request,
        response: Response,
        _input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init create {ITEM}")
    service = Service(api_response, main_db) ##
    item_db = await service.add(_input, token.restaurantes) ##
    api_response.logger.info(f"Finish create {ITEM}: {item_db}") ##
    return item_db

@general_menu_router.get(
    "",
    tags=["General Menu"],
    description=f"Get {ITEM}s"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get(
    request:Request,
    response:Response,
    api_response=Depends(ApiResponse),
    main_db=Depends(get_mongo_db),
    token: str = Depends(get_user_current),
) -> ResponseBase[list[Model]]:
    api_response.logger.info(f"Init get all {ITEM}")
    service = Service(api_response, main_db)
    items_db = await service.get()
    api_response.logger.info(f"Finish get {ITEM}: {items_db}")
    return items_db

###hasta aca
@general_menu_router.get(
    "/{general_menu_id}",
    tags=["General Menu"],
    description="Retrieve a general menu by its ID, including associated articles.",
    responses={
        200: {
            "description": "Successful response with menu details.",
            "content": {
                "application/json": {
                    "example": {
                        "status_code": 200,
                        "data": {
                            "restaurant_id": "d5625afe-2e5d-45f4-ab52-982a79daf173",
                            "name": "Menu General",
                            "description": "Menu general diario en condiciones normaless",
                            "final_articles": [
                                {
                                    "id": "46eea73d-6616-4178-8c3b-f9c16cc2b147",
                                    "name": "Pizzas",
                                    "articles": [
                                        {
                                            "id": "78667d65-7c15-4f7b-8216-3b1ae151ebeb",
                                            "name": "Pizza Anchoas",
                                            "description": "Pizza",
                                            "options": [],
                                            "price": 10
                                        },
                                        {
                                            "id": "7f77600c-d8ce-4daf-8208-2ff1a54978ca",
                                            "name": "Pizza de la casa",
                                            "description": "pizza con queso lalala ",
                                            "options": [],
                                            "price": 15
                                        }
                                    ]
                                },
                                {
                                    "id": "ef32fa4a-9a32-4699-85b9-c3d7c1b40772",
                                    "name": "Pastas",
                                    "articles": [
                                        {
                                            "id": "b96913e2-68e1-40aa-9076-7e79a4312820",
                                            "name": "Pastas",
                                            "description": "Pastas",
                                            "options": [
                                                {
                                                    "id": "56e22737-5987-45bf-a2ad-1b67f1442337",
                                                    "display_name": "bolognesa",
                                                    "unit": "gr",
                                                    "quantity": 100,
                                                    "price": 10
                                                },
                                                {
                                                    "id": "f7e40e1d-16fc-4466-8fbc-e01bb3c4dfc1",
                                                    "display_name": "larala",
                                                    "unit": "gr",
                                                    "quantity": 150,
                                                    "price": 5
                                                },
                                                {
                                                    "id": "bde960ab-5375-4e5e-aef1-9d493ca044e9",
                                                    "display_name": "asdasd",
                                                    "unit": "gr",
                                                    "quantity": 120,
                                                    "price": 7
                                                }
                                            ],
                                            "price": 10
                                        }
                                    ]
                                }
                            ],
                            "daily_menu": []
                        },
                        "errors": [],
                        "request_id": "ec189316-2941-4803-853e-a6408b0afc72"
                    }
                }
            }
        }
    }
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        general_menu_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[MenuResponse]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    ##
    menu_data = await service.get_menu_with_articles(general_menu_id)
    ##
    #item_db = await service.get_by_id(general_menu_id)
    api_response.logger.info(f"Finish get {ITEM}: {menu_data}")
    return menu_data

@general_menu_router.patch(
    "/{general_menu_id}",
    tags=["General Menu"],
    description=f"Modify {ITEM} by id (searches for General Menu id then modifies it)"
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_by_id(
        request: Request,
        response: Response,
        general_menu_id: str,
        modify_input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[MenuResponse]:
    api_response.logger.info(f"Init modify {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.change(general_menu_id, modify_input)
    api_response.logger.info(f"Finish modify {ITEM}: {item_db}")
    
    return item_db



@general_menu_router.delete(
    "/{general_menu_id}",
    tags=["General Menu"],
    description=f"Delete {ITEM} by id (searches dor General Menu id then deletes it)"
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        general_menu_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(general_menu_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return item_db
