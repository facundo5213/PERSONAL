from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db
from api.stock.stock_service import StockService as Service
from models.stock import StockModel as Model
from schemas.stock import StockInput as Input
from utils.exceptions.response_handler import response_handler
from schemas.response import ResponseBase
from utils.presentation.response import ApiResponse

from utils.oauth.auth import get_user_current



ITEM = "stock"

###################################################################################################

stock_router: APIRouter = APIRouter(prefix="/v1/stock")

@stock_router.post(
    "",
    tags=["Stock"],
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

@stock_router.get(
    "",
    tags=["Stock"],
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


@stock_router.get(
    "/{stock_id}",
    tags=["Stock"],
    description=f"Get {ITEM} by id"
)


@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        stock_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.get_by_id(stock_id)
    api_response.logger.info(f"Finish get {ITEM}: {item_db}")
    return item_db

@stock_router.patch(
    "/{stock_id}",
    tags=["Stock"],
    description=f"Modify {ITEM} by id"
)


@response_handler(response_status=status.HTTP_200_OK)
async def modify_by_id(
        request: Request,
        response: Response,
        stock_id: str,
        modify_input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init modify {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.change(stock_id, modify_input)
    api_response.logger.info(f"Finish modify {ITEM}: {item_db}")
    return item_db


@stock_router.delete(
    "/{stock_id}",
    tags=["Stock"],
    description=f"Delete {ITEM} by id"
)

@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        stock_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(stock_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return 
