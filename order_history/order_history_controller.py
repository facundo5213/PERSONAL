from fastapi import APIRouter, Request, Response, status, Depends
from models.users import UserResponseModel
from api.order_history.order_history_service import OrderHistoryService
from core.db import get_mongo_db
from models.order_history import OrderHistoryModel
from schemas.response import ResponseBase
from schemas.order_history import OrderHistoryInput
from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse

from utils.oauth.auth import get_user_current

order_history_router: APIRouter = APIRouter(prefix="/v1/order_history")


@order_history_router.post(
    "",
    tags=["Order History"]
)
@response_handler(response_status=status.HTTP_201_CREATED)
async def create_order_history(
        request: Request,
        response: Response,
        orders_history_input: OrderHistoryInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[OrderHistoryModel]:
    api_response.logger.info("Init create order history")
    order_history_service = OrderHistoryService(api_response, main_db)
    order_history = await order_history_service.add_order_history(orders_history_input, token.restaurantes)
    api_response.logger.info(f"Finish create order history: {order_history}")
    return order_history


@order_history_router.get(
    "",
    tags=["Order History"],
    description="Get all order histories"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_order_histories(
        request: Request,
        response: Response,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[list[OrderHistoryModel]]:
    api_response.logger.info("Init get all order histories")
    order_history_service = OrderHistoryService(api_response, main_db)
    order_histories = await order_history_service.get_order_histories()
    api_response.logger.info(f"Finish get order histories: {order_histories}")
    return order_histories


@order_history_router.get(
    "/{order_history_id}",
    tags=["Order History"],
    description="Get order history by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_order_history(
        request: Request,
        response: Response,
        order_history_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[OrderHistoryModel]:
    api_response.logger.info("Init get order history")
    order_history_service = OrderHistoryService(api_response, main_db)
    order_history = await order_history_service.get_order_history_by_id(order_history_id)
    api_response.logger.info(f"Finish get order history: {order_history}")
    return order_history


@order_history_router.patch(
    "/{order_history_id}",
    tags=["Order History"],
    description="Modify order history by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_order_history(
        request: Request,
        response: Response,
        order_history_id: str,
        modify_order_history_input: OrderHistoryInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[OrderHistoryModel]:
    api_response.logger.info("Init modify order history")
    order_history_service = OrderHistoryService(api_response, main_db)
    order_history = await order_history_service.change_order_history(order_history_id, modify_order_history_input)
    api_response.logger.info(f"Finish modify order history: {order_history}")
    return order_history


@order_history_router.delete(
    "/{order_history_id}",
    tags=["Order History"],
    description="Delete order history by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_order_history(
        request: Request,
        response: Response,
        order_history_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase:
    api_response.logger.info("Init delete order history")
    order_history_service = OrderHistoryService(api_response, main_db)
    order_history = await order_history_service.delete_order_history_by_id(order_history_id)
    api_response.logger.info(f"Finish delete order history: {order_history}")
    return
