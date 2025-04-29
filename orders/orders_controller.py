from fastapi import APIRouter, Request, Response, status, Depends
from models.users import UserResponseModel
from api.orders.orders_service_v2 import OrdersService
from core.db import get_mongo_db
from models.orders import OrdersModel
from schemas.response import ResponseBase
from schemas.orders import OrdersInput
from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse

from utils.oauth.auth import get_user_current

orders_router: APIRouter = APIRouter(prefix="/v1/orders")


@orders_router.post(
    "",
    tags=["Orders"],
    summary="Crear una nueva orden",
    description="Endpoint para crear una nueva orden en el sistema.",
    response_description="La orden creada."
)
@response_handler(response_status=status.HTTP_201_CREATED)
async def create_orders(
        request: Request,
        response: Response,
        orders_input: OrdersInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[OrdersModel]:
    api_response.logger.info("Init create order")
    order_service = OrdersService(api_response, main_db)
    order = await order_service.add_order(orders_input, token.restaurantes)
    api_response.logger.info(f"Finish create order: {order}")
    return order


@orders_router.get(
    "",
    tags=["Orders"],
    summary="Obtener todas las órdenes",
    description="Endpoint para obtener todas las órdenes del sistema.",
    response_description="Una lista de órdenes.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_orders(
        request: Request,
        response: Response,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[list[OrdersModel]]:
    api_response.logger.info("Init get all orders")
    order_service = OrdersService(api_response, main_db)
    orders = await order_service.get_orders()
    api_response.logger.info(f"Finish get orders: {orders}")
    return orders


@orders_router.get(
    "/{order_id}",
    tags=["Orders"],
    summary="Obtener orden por ID",
    description="Endpoint para obtener una orden por su ID.",
    response_description="La orden con el ID especificado.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_order(
        request: Request,
        response: Response,
        order_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[OrdersModel]:
    api_response.logger.info("Init get order")
    order_service = OrdersService(api_response, main_db)
    order = await order_service.get_order_by_id(order_id)
    api_response.logger.info(f"Finish get order: {order}")
    return order


@orders_router.patch(
    "/{order_id}",
    tags=["Orders"],
    summary="Modificar orden por ID",
    description="Endpoint para modificar una orden por su ID.",
    response_description="La orden modificada."
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_orders(
        request: Request,
        response: Response,
        order_id: str,
        modify_orders_input: OrdersInput,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[OrdersModel]:
    api_response.logger.info("Init modify order")
    order_service = OrdersService(api_response, main_db)
    order = await order_service.change_order(order_id, modify_orders_input)
    api_response.logger.info(f"Finish modify order: {order}")
    return order


@orders_router.delete(
    "/{order_id}",
    tags=["Orders"],
    summary="Eliminar orden por ID",
    description="Endpoint para eliminar una orden por su ID.",
    response_description="La orden eliminada.",
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_order(
        request: Request,
        response: Response,
        order_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase:
    api_response.logger.info("Init delete order")
    order_service = OrdersService(api_response, main_db)
    order = await order_service.delete_order_by_id(order_id)
    api_response.logger.info(f"Finish delete order: {order}")
    return
