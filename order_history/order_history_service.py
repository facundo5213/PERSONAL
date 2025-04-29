from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.presentation.errors import NotFoundException
from models.order_history import OrderHistoryModel
from repositories.order_history import OrderHistoryRepository
from schemas.order_history import OrderHistoryInput, OrderHistoryInputComplete
from utils.presentation.response import ApiResponse


class OrderHistoryService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.repository = OrderHistoryRepository(self.main_db)

    async def add_order_history(self, input: OrderHistoryInput, restaurant_id) -> OrderHistoryModel:
        self.api_response.logger.info(f"Create order_history_db in db.")

        input_data = input.model_dump()
        input_data["restaurant_id"] = restaurant_id 
        input_model = OrderHistoryInputComplete.model_validate(input_data)

        order_history_db = await self.repository.create(input_model)
        self.api_response.logger.info(f"order_history_db: {order_history_db}")
        return order_history_db

    async def get_order_histories(self) -> list[OrderHistoryModel]:
        self.api_response.logger.info("Init get order history from db.")
        order_history_db = await self.repository.get_all_actives()
        self.api_response.logger.info(f"order_history_db: {order_history_db}")
        return order_history_db

    async def get_order_history_by_id(self, order_history_id: str) -> OrderHistoryModel:
        self.api_response.logger.info(f"Init get order history from db, order_history_id: {order_history_id}")
        order_history_db = await self.repository.get_active_by_id(order_history_id)
        self.api_response.logger.info(f"order_history_db: {order_history_db}")
        return order_history_db

    async def change_order_history(self, order_history_id: str, modify_order_history_input: OrderHistoryInput) -> OrderHistoryModel:
        self.api_response.logger.info(f"Get order history from db, order_history_id: {order_history_id}")
        order_history_db = await self.repository.get_active_by_id(order_history_id)
        self.api_response.logger.info(f"order_history_db: {order_history_db}")
        self.api_response.logger.info(f"Patch order_history_db in db.")
        order_history_db = await self.repository.patch(order_history_id, modify_order_history_input)
        self.api_response.logger.info(f"order_history_db: {order_history_db}")
        return order_history_db

    async def delete_order_history_by_id(self, order_history_id: str) -> None:
        self.api_response.logger.info(f"Init delete order history from db, order_history_db: {order_history_id}")
        await self.repository.soft_delete(order_history_id)
