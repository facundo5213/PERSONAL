from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from utils.presentation.errors import NotFoundException
from models.orders import OrdersModel
from repositories.orders import OrdersRepository
from repositories.stock import StockRepository
from schemas.stock import StockInput
from schemas.orders import OrdersInput, OrdersInputComplete
from utils.presentation.response import ApiResponse
from utils.presentation.errors import TransactionException
from api.orders.order_transaction_service import TransactionService

from api.stock.stock_service import StockService
from api.order_history.order_history_service import OrderHistoryService

class OrdersService:
    def __init__(self, api_response: ApiResponse, main_db: AsyncIOMotorDatabase):
        self.api_response = api_response
        self.main_db = main_db
        self.orders_repository = OrdersRepository(self.main_db)
        self.order_transaction_service = TransactionService(
            api_response = api_response,
            stock_service = StockService,
            order_history_service = OrderHistoryService,
            main_db = main_db
        )

    async def check_stock_availability(self, orders_input: OrdersInput) -> list:
        insufficient_items = []
    
    # Revisa si hay elementos insuficientes
        for item in orders_input.menu_items:
            stock_item = await self.main_db.stock.find_one({"_id": item.final_article_id})
            if stock_item and stock_item["quantity"] < item["quantity"]:
                insufficient_items.append(f"Article {stock_item['name']}")
        
        # Checkea options
        for item in orders_input.menu_items:
            for option_id in item.options:
                stock_item = await self.main_db.stock.find_one({"_id": option_id})
                if stock_item and stock_item["quantity"] < 1:
                    insufficient_items.append(f"Option {stock_item['name']}")
        
        return insufficient_items
    
    async def order_deduction_from_stock(self, orders_input: OrdersInput, restaurant_id) -> OrdersInput: #Crea transaccion del stock para restar monto de ingredientes
        try:                                                   
            async with await self.main_db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        order_db = await self.orders_repository.create(input_model, session=session)
                        # Actualiza stock 
                        await self.stock_service.order_substraction(final_article_list, options_list, session)
                        # Commit transaction
                        await session.commit()
                        return order_db
                except Exception as e:
                    await session.abort_transaction()
                    raise TransactionException(f"Error during transaction: {str(e)}")
        except Exception as e:
            self.api_response.logger.error(f"Order creation failed: {str(e)}")
            raise TransactionException(f"Error during order creation: {str(e)}")
    
    async def add_order(self, orders_input: OrdersInput, restaurant_id) -> OrdersModel:
        self.api_response.logger.info(f"Create order_db in db.")

        """ Validaciones """
        # Valido la existencia de la Table asignada
        if orders_input.table_id != None:
            existing_table = await self.main_db.tables.find_one({"_id": orders_input.table_id})
            if not existing_table:
                raise NotFoundException("Invalid table_id")
        # Valido la existencia de los Final Articles asignadas en menu_items
        # (Sus opciones elegidas se validan al momento de buscar los precios)
        for item in orders_input.menu_items:
            existing_item = await self.main_db.final_articles.find_one({"_id": item.final_article_id})
            if not existing_item:
                raise NotFoundException(f"The final_articles's id <{item.final_article_id}> is invalid")
        # Valido la existencia de los menu_id
        for menu_group in orders_input.menu_groups:
            existing_item = await self.main_db.daily_menu.find_one({"_id": menu_group.menu_id})
            if not existing_item:
                raise NotFoundException(f"The menu's id <{menu_group.menu_id}> is invalid")
            # Valido la existencia de los Final Articles asignados en cada menu_group
            for final_article_in_menu in menu_group.items:
                # Validamos la existencia de cada artículo final (final_article_id)
                existing_item = await self.main_db.final_articles.find_one({"_id": final_article_in_menu.final_article_id})
                if not existing_item:
                    raise NotFoundException(f"The final_articles's id <{final_article_in_menu.final_article_id}> in menu_group <{menu_group.menu_id}> is invalid")
                # Validar opciones (si hay opciones seleccionadas) de los Final Articles asignados en cada menu_group
                if final_article_in_menu.options:
                    for option_id in final_article_in_menu.options:
                        option = None
                        for opt in existing_item["options"]:
                            if opt["id"] == option_id:
                                option = opt
                                break
                        if not option:
                            raise NotFoundException(
                                f"Option id <{option_id}> is invalid for final_article <{final_article_in_menu.final_article_id}> in menu_group <{menu_group.menu_id}>"
                            )
        
        insufficient_items = await self.check_stock_availability(orders_input)
        if insufficient_items:
            raise StockInsufficientException(f"Insufficient stock for: {', '.join(insufficient_items)}")
        #Checkeo si hay suficiente para crear el plato
                       
        """ Fin de las validaciones"""
        """ Búsqueda de precios """
        """ También enumeración de platos y menús y validación de opciones de final_articles individuales """
        """ También comenzamos a guardar en una variable todos los ids de cada final_article y opciones tantas veces como quantity,
        ya sea de menu_items como de menu_groups, para ser enviados por medio de la transacción al service de stock para
        hacer el respectivo descuento """
        # Rastreo los precios de los menu_items y sus options
        input_data = orders_input.model_dump()  # Primero convertimos el modelo en un diccionario
        parcial_price = 0.00  # Inicializamos el precio parcial
        item_numeration = 0  # Numeración de cada final_article
        menu_numeration = 0  # Numeración de cada daily_menu
        final_article_list = []
        options_list = []
            # Iteramos sobre los items de menú_items (final_articles)
        for item in input_data["menu_items"]:
            final_article = await self.main_db.final_articles.find_one({"_id": item["final_article_id"]})
            
            for i in range(item["quantity"]):  # Guardamos los ids de los final_article tantas veces como quantity
                final_article_list.append(item["final_article_id"])  
                item_numeration += 1 # Incrementamos variable para enumerar el item
                # Agregamos la variable que enumera cada item de menu_items
                item["item_number"] = item_numeration
                # Agregamos la variable del precio a cada item de menu_items
                item["price"] = final_article["price"]  # Agregamos el precio al item en el diccionario
                    
                # Validar y sumar los precios de las opciones seleccionadas si las hay
                for option_id in item["options"]:
                    for i in range(item["quantity"]):  # Guardamos los ids de los options tantas veces como quantity
                        options_list.append(option_id)  
                    option = None
                    for opt in final_article["options"]:
                        if opt["id"] == option_id:
                            option = opt
                            break
                    if not option:
                        raise NotFoundException(f"Option id <{option_id}> is invalid for final_article <{item['final_article_id']}>")
                    item["price"] += option["modificador_precio"]  # Sumamos al precio del final_article cada una de las opciones
                
                # Acumulamos el precio de cada uno de los final_articles con sus opciones y cantidades
                parcial_price += item["price"] * item["quantity"]


            # Rastreo los precios de los menu_groups
            # Iteramos sobre los items de menú
            for menu_group in input_data["menu_groups"]:
                menu = await self.main_db.daily_menu.find_one({"_id": menu_group["menu_id"]})
                if not menu:
                    raise NotFoundException(f"The menu's id <{menu_group['menu_id']}> is invalid")
                
                menu_numeration += 100 # Incrementamos variable para enumerar el item
                
                # Agregamos la variable que enumera cada menu_items
                menu_group["menu_number"] = menu_numeration
                # Agregamos la variable del precio a cada menu_group
                menu_group["price"] = menu["special_price"]

                # Acumulamos el precio de cada uno de los menu_groups
                parcial_price += menu_group["price"]


                # Reseteamos a "0" la variable de enumeración de items para numerar los items dentro de sus menu_groups
                # Cada vez que se termina de enumerar los items de un menu_group, se resetea nuevamente para enumerar el próximo menu_group
                item_numeration = 0

                # Enumeramos los items (final_articles) de cada menu_group
                for final_article_in_menu_group in menu_group["items"]:

                    for i in range(final_article_in_menu_group["quantity"]):  # Guardamos los ids de los final_article tantas veces como quantity
                        final_article_list.append(final_article_in_menu_group["final_article_id"])  

                    item_numeration += 1
                    # Agregamos la variable que enumera cada item de menu_items
                    final_article_in_menu_group["item_number"] = menu_numeration + item_numeration

                    # Si hay opciones, guardamos su id
                    for option_id in final_article_in_menu_group["options"]:
                        for i in range(final_article_in_menu_group["quantity"]):  # Guardamos los ids de los options tantas veces como quantity
                            options_list.append(option_id)

               
            # Creamos la variable amount y le asignamos el precio acumulado de los menu_items y menu_groups
            input_data["amount"] = parcial_price
            # # Modelamos el objeto para agregarle los datos necesarios (restaurant_id, precios)
            input_data["restaurant_id"] = restaurant_id 
            input_model = OrdersInputComplete.model_validate(input_data)
            order_deduction = await self.order_deduction_from_stock(orders_input, restaurant_id)

    async def get_orders(self) -> list[OrdersModel]:
        self.api_response.logger.info("Init get orders from db.")
        orders_db = await self.orders_repository.get_all_actives()
        self.api_response.logger.info(f"orders_db: {orders_db}")
        return orders_db

    async def get_order_by_id(self, order_id: str) -> OrdersModel:
        self.api_response.logger.info(f"Init get order from db, order_id: {order_id}")
        order_db = await self.orders_repository.get_active_by_id(order_id)
        self.api_response.logger.info(f"order_db: {order_db}")
        return order_db

    async def change_order(self, order_id: str, modify_orders_input: OrdersInput) -> OrdersModel:
        self.api_response.logger.info(f"Get order from db, order_id: {order_id}")
        order_db = await self.orders_repository.get_active_by_id(order_id)
        self.api_response.logger.info(f"order_db: {order_db}")
        self.api_response.logger.info(f"Patch order_db in db.")
        order_db = await self.orders_repository.patch(order_id, modify_orders_input)
        self.api_response.logger.info(f"order_db: {order_db}")
        return order_db

    async def delete_order_by_id(self, order_id: str) -> None:
        self.api_response.logger.info(f"Init delete order from db, order_id: {order_id}")
        await self.orders_repository.soft_delete(order_id)
