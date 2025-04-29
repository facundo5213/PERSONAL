from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from datetime import datetime

# Conexión al cliente
uri = "mongodb://localhost:27017"
client = MongoClient(uri)

# Define las bases de datos y colecciones
orders_collection = client.restaurant.orders
order_history_collection = client.restaurant.orderHistory
stock_collection = client.restaurant.stock

# WriteConcern para asegurar que las escrituras sean confirmadas
wc_majority = WriteConcern("majority", wtimeout=1000)

def process_order(order_data):
    """
    order_data:
    {
        "order_id": "12345",
        "customer_name": "John Doe",
        "items": [
            {"product_id": "item_1", "quantity": 2},
            {"product_id": "item_2", "quantity": 1}
        ],
        "employee_id": "emp_001"
    }
    """
    try:
        with client.start_session() as session:
            # Maneja la transacción
            with session.start_transaction(
                read_concern=ReadConcern("snapshot"),
                write_concern=wc_majority,
                read_preference=ReadPreference.PRIMARY
            ):
                # Paso 1: Registrar la orden en orders
                orders_collection.insert_one(order_data, session=session)

                # Paso 2: Registrar el historial en orderHistory
                order_history_data = {
                    "order_id": order_data["order_id"],
                    "employee_id": order_data["employee_id"],
                    "action": "CREATED",
                    "timestamp": datetime.now(datetime.timezone.utc),
                    "details": order_data
                }
                order_history_collection.insert_one(order_history_data, session=session)

                # Paso 3: Actualizar el inventario en stock
                for item in order_data["items"]:
                    product_id = item["product_id"]
                    quantity = item["quantity"]

                    # Buscar el producto y verificar disponibilidad
                    stock_item = stock_collection.find_one({"product_id": product_id}, session=session)
                    if not stock_item or stock_item["quantity"] < quantity:
                        raise Exception(f"Stock insuficiente para el producto {product_id}")

                    # Reducir el inventario
                    stock_collection.update_one(
                        {"product_id": product_id},
                        {"$inc": {"quantity": -quantity}},
                        session=session
                    )

                print("Transacción completada exitosamente.")

    except PyMongoError as e:
        print(f"Error durante la transacción: {str(e)}")
        raise
