# from pymongo import ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from utils.presentation.errors import TransactionException
# from api.orders.orders_service import OrdersService
from api.stock.stock_service import StockService
from api.order_history.order_history_service import OrderHistoryService
from schemas.orders import OrdersInputComplete
from repositories.orders import OrdersRepository
from utils.presentation.response import ApiResponse
from core.db import get_mongo_client

class TransactionService:
    def __init__(self,
                 api_response: ApiResponse,
                 stock_service: StockService, 
                 order_history_service: OrderHistoryService, 
                 main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.stock_service = stock_service
        self.order_history_service = order_history_service
        self.mongo_client = get_mongo_client()
        self.main_db = main_db
        self.orders_repository = OrdersRepository(self.main_db)

    async def create_order_transaction(self, orders_input: OrdersInputComplete, final_article_list, options_list, restaurant_id):
        """
        Orquesta la creación de una orden, actualiza el inventario y registra el historial de la orden en una transacción.
        Args:
            orders_input (OrdersInputComplete): Entrada con los datos de la orden.
            final_article_list (list):  Lista de IDs de artículos finales involucrados en la orden. 
                                        Cada ID repetido tantas veces como fue pedido
            options_list (list): Lista de IDs de opciones seleccionadas. Cada ID repetido tantas veces como fue pedido
            restaurant_id (str): ID del restaurante asociado con la orden.
        Returns:
            dict: Documento de la orden creada.
        Raises:
            TransactionException: Si ocurre algún error durante la transacción.
        """
        self.api_response.logger.info(f"Initiating transaction for restaurant_id: {restaurant_id}")

        try:
            # Inicia una sesión de transacción
            async with await self.mongo_client.start_session() as session:
                self.api_response.logger.info("Session started successfully.")
                async with session.start_transaction():
                    self.api_response.logger.info("Transaction started.")

                    # 1. Crea la orden en la colección Orders
                    self.api_response.logger.debug(f"Creating order with data: {orders_input}")
                    order_db = await self.orders_repository.create(orders_input, session=session)
                    self.api_response.logger.info(f"Order created successfully: {order_db.id}")
                    self.api_response.logger.info("Transaction committed successfully.")
                    return order_db

        except Exception as e:
            # Manejo de errores en la transacción
            self.api_response.logger.error(f"Transaction failed: {str(e)}")
            self.api_response.logger.error(f"Transaction Aborted")
            raise TransactionException(f"Error during transaction: {str(e)}")
        
        finally:
            # Fin de la sesión y transacción
            self.api_response.logger.info("Ending session.")
        
        
