from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db
from api.receipt.receipt_service import ReceiptService as Service
from models.receipt import ReceiptModel as Model
from schemas.receipt import ReceiptInput as Input
from utils.exceptions.response_handler import response_handler
from schemas.response import ResponseBase
from utils.presentation.response import ApiResponse

from utils.oauth.auth import get_user_current



ITEM = "receipt"

###################################################################################################

receipt_router: APIRouter = APIRouter(prefix="/v1/receipt")

@receipt_router.post(
    "",
    tags=["receipt"],
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

@receipt_router.get(
    "",
    tags=["receipt"],
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


@receipt_router.get(
    "/{receipt_id}",
    tags=["receipt"],
    description=f"Get {ITEM} by id"
)


@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        receipt_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.get_by_id(receipt_id)
    api_response.logger.info(f"Finish get {ITEM}: {item_db}")
    return item_db

@receipt_router.delete(
    "/{receipt_id}",
    tags=["receipt"],
    description=f"Delete {ITEM} by id"
)

@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        receipt_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(receipt_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return 
