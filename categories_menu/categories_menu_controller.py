from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db

from api.categories_menu.categories_menu_service import CategoriesMenuService as Service

from models.categories_menu import CategoriesMenuModel  as Model, CategoriesMenuModelResponseId
from models.users import UserResponseModel

from schemas.categories_menu import CategoriesMenuInput as Input
from schemas.response import ResponseBase

from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse
from utils.oauth.auth import get_user_current


ITEM = "categories_menu"

###################################################################################################

categories_menu_router: APIRouter = APIRouter(prefix="/v1/categories_menu")

@categories_menu_router.post(
    "",
    tags=["Categories Menu"],
    description=f"Create {ITEM} (creates Category Menu)"
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


@categories_menu_router.get(
    "",
    tags=["Categories Menu"],
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


@categories_menu_router.get(
    "/{categories_menu_id}",
    tags=["Categories Menu"],
    description=f"Get {ITEM} by id (searches Category Menu by id then retrives it)"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        categories_menu_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[CategoriesMenuModelResponseId]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.get_by_id(categories_menu_id)
    api_response.logger.info(f"Finish get {ITEM}: {item_db}")
    return item_db


@categories_menu_router.patch(
    "/{categories_menu_id}",
    tags=["Categories Menu"],
    description=f"Modify {ITEM} by id (searches for Category Menu id and modifies it)"
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_by_id(
        request: Request,
        response: Response,
        categories_menu_id: str,
        modify_input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init modify {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.change(categories_menu_id, modify_input)
    api_response.logger.info(f"Finish modify {ITEM}: {item_db}")
    return item_db


@categories_menu_router.delete(
    "/{categories_menu_id}",
    tags=["Categories Menu"],
    description=f"Delete {ITEM} by id (searches for Category Menu and then deletes it)"
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        categories_menu_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(categories_menu_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return item_db
