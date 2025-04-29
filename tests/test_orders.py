import pytest
from fastapi import status
from core.config import settings
import os
from tests.test_user import get_access_token
from tests.test_restaurants import get_restaurant_id

order_id_global = None
restaurant_id_fixture = get_restaurant_id
table_id_fixture = "false_id_table" # get_table_id

# """ Función para crear un Restaurant y obtener el id.
# Esta función la utilizarán todos los módulos para obtener 
# el id que permite cubrir las dependencias
# """
# @pytest.fixture(scope="session")
# def get_rooms_id(client, get_access_token, get_restaurant_id):
#     """Obtenemos el token y creamos el Restaurant"""
#     # Primero logueamos y obtenemos el token
#     #token = get_access_token
#     #restaurant_id = get_restaurant_id
#     # Encabezados con el token válido
#     headers = {"Authorization": f"Bearer {get_access_token}"}

#     room_data = {
#         "room_number": 99,
#         "description": "string",
#         #"tables": [],
#         "restaurant_id": get_restaurant_id
#     }
    
#     response = client.post("/api/v1/rooms", json=room_data, headers=headers)
#     print(f' ESTO ES TUNA PRUEBA DE COMO ARMA EL RESPONSE ROOMS {response}')
#     # Extraemos el id de la respuesta y lo devolvemos
#     yield response.json()["data"]["_id"]



# Test para crear una Order en una Table existente de un Restaurante existente
def test_create_orders(client, get_access_token, restaurant_id_fixture):
    """Prueba para el endpoint POST /v1/orders."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    order_data = {
        "restaurant_id": restaurant_id_fixture,
        "table_id": table_id_fixture,
        "menu_items": [{"id_menu_item_1": 1},
                       {"id_menu_item_2": 4},
                       {"id_menu_item_456": 2}
                       ], # A dictionary with menu item IDs as keys and quantities as values
        "datetime": "string",
        "comments": "string",
        "amount": 1.00,
        "status": "string"
    }
    
    response = client.post("/api/v1/orders", json=order_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    # Extraemos el ID y lo almacenamos en la variable global
    global order_id_global  # Usar la variable global para almacenar el ID
    order_id_global = response.json()["data"]["_id"]
    print(f"Order ID: {order_id_global}")


# Test para crear una Table en un Restaurant inexistente
def test_create_order_with_invalid_restaurant_id(client, get_access_token):
    """Prueba para el endpoint POST /v1/orders."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    order_data = {
        "restaurant_id": "invalid_restaurant_id", # Valor inválido de restaurant_id
        "table_id": table_id_fixture,
        "menu_items": [], # A dictionary with menu item IDs as keys and quantities as values
        "datetime": "string",
        "comments": "string",
        "amount": 1.00,
        "status": "string"
    }
    
    response = client.post("/api/v1/orders", json=order_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


"""Tengo que tener la verificacion en el service para poder probarlo,
y eso lo voy a tener poder usar cuando pueda tener el table_id_fixture"""
# # Test para crear una Table en un Restaurant inexistente
# def test_create_table_with_invalid_table_id(client, get_access_token, restaurant_id_fixture):
#     """Prueba para el endpoint POST /v1/orders."""
#     # Primero logueamos y obtenemos el token
#     token = get_access_token
#     # Encabezados con el token válido
#     headers = {"Authorization": f"Bearer {token}"}

#     print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
#     env_value = os.getenv("ENV")
#     print(f"Valor de ENV: {env_value}")
#     order_data = {
#         "restaurant_id": restaurant_id_fixture,
#         "table_id": "invalid_table_id",# Valor inválido de table_id
#         "menu_items": [], # A dictionary with menu item IDs as keys and quantities as values
#         "datetime": "string",
#         "comments": "string",
#         "amount": 1.00,
#         "status": "string"
#     }
    
#     response = client.post("/api/v1/orders", json=order_data, headers=headers)
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# Test para pedir las Rooms
def test_get_orders(client, get_access_token):
    """Prueba para el endpoint GET /v1/orders."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/orders", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_order(response_data, True)
    

# Test para pedir una Order por id
def test_get_order_by_id(client, get_access_token):
    """Prueba para el endpoint GET /v1/orders/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/api/v1/orders/{order_id_global}", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_order(response_data)


# # Test para modificar una Order por id
# def test_patch_order_by_id(client, get_access_token, restaurant_id_fixture):
#     """Prueba para el endpoint PATCH /v1/rooms/{id}."""
#     # Primero logueamos y obtenemos el token
#     token = get_access_token
#     # Encabezados con el token válido
    
#     headers = {"Authorization": f"Bearer {token}"}
    
#     order_data = {
#         "restaurant_id": restaurant_id_fixture,
#         "table_id": table_id_fixture,
#         "menu_items": [{"id_menu_item_1": 1},
#                        {"id_menu_item_2": 4},
#                        {"id_menu_item_456": 2}
#                        ], # A dictionary with menu item IDs as keys and quantities as values
#         "datetime": "string",
#         "comments": "string",
#         "amount": 1.00,
#         "status": "string"
#     }

#     response = client.patch(f"/api/v1/rooms/{room_id_global}", json=room_data, headers=headers)
    
#     # Verificar que la respuesta sea HTTP 200 OK
#     assert response.status_code == status.HTTP_200_OK

#     # Verificamos que la modificación en "description" se haya efectuado correctamente
#     check_modification = response.json()["data"]
#     assert check_modification["description"] == "string_modified"


# # Test para eliminar una Room por id
# def test_delete_room_by_id(client, get_access_token):
#     """Prueba para el endpoint DELETE /v1/rooms/{id}."""
#     # Primero logueamos y obtenemos el token
#     token = get_access_token
#     # Encabezados con el token válido
#     headers = {"Authorization": f"Bearer {token}"}

#     response = client.delete(f"/api/v1/rooms/{room_id_global}", headers=headers)
    
#     # Verificar que la respuesta sea HTTP 200 OK
#     assert response.status_code == status.HTTP_200_OK

#     # Verificamos que la eliminación del objeto Room se haya efectuado correctamente
#     check_modification = response.json()["data"]
#     assert check_modification["is_deleted"] == True
#     for table in  check_modification["tables"]:
#         assert table["is_deleted"] == True





# Funcion para verificar el cuerpo de las Rooms
def verificacion_data_order(response, data_is_list = False):
    assert "status_code" in response
    assert "errors" in response
    assert "request_id" in response
    assert "data" in response
    if data_is_list:
        assert isinstance(response["data"], list)
    else:
        assert isinstance(response["data"], dict)

    # Verificar que los campos dentro de "data" estén presentes y correctos
    if response["data"]:  # Solo si hay usuarios en la respuesta
        if data_is_list:
            room = response["data"][0]
        else:
            room = response["data"]
        
        assert "_id" in room
        assert "created_at" in room
        assert "updated_at" in room
        assert "is_deleted" in room
        assert "restaurant_id" in room
        assert "table_id" in room
        assert "menu_items" in room
        assert isinstance(room["menu_items"], list)
        assert "datetime" in room
        assert "comments" in room
        assert "amount" in room
        assert "status" in room
        