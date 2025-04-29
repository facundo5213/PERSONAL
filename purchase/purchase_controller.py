from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db
from api.purchase.purchase_service import PurchaseService as Service
from models.purchase import PurchaseModel as Model
from schemas.purchase import PurchaseInput as Input
from utils.exceptions.response_handler import response_handler
from schemas.response import ResponseBase
from utils.presentation.response import ApiResponse

from utils.oauth.auth import get_user_current



ITEM = "purchase"

###################################################################################################

purchase_router: APIRouter = APIRouter(prefix="/v1/purchase")

@purchase_router.post(
    "",
    tags=["purchase"],
    description=f"Create {ITEM}"
)
@response_handler(response_status=status.HTTP_200_OK)
async def create(
        request: Request,
        response: Response,
        _input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init create {ITEM}")
    service = Service(api_response, main_db) ##
    item_db = await service.add(_input) ##
    api_response.logger.info(f"Finish create {ITEM}: {item_db}") ##
    return item_db

@purchase_router.get(
    "",
    tags=["purchase"],
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


@purchase_router.get(
    "/{purchase_id}",
    tags=["purchase"],
    description=f"Get {ITEM} by id"
)


@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        purchase_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.get_by_id(purchase_id)
    api_response.logger.info(f"Finish get {ITEM}: {item_db}")
    return item_db

@purchase_router.delete(
    "/{purchase_id}",
    tags=["purchase"],
    description=f"Delete {ITEM} by id"
)

@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        purchase_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(purchase_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return 
