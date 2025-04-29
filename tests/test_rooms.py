import pytest
from fastapi import status
from core.config import settings
import os
from tests.test_user import get_access_token
from tests.test_restaurants import get_restaurant_id

room_id_global = None
#restaurant_id_fixture = get_restaurant_id


""" Función para crear un Restaurant y obtener el id.
Esta función la utilizarán todos los módulos para obtener 
el id que permite cubrir las dependencias
"""
@pytest.fixture(scope="session")
def get_rooms_id(client, get_access_token, get_restaurant_id):
    """Obtenemos el token y creamos el Restaurant"""
    # Primero logueamos y obtenemos el token
    #token = get_access_token
    #restaurant_id = get_restaurant_id
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {get_access_token}"}

    room_data = {
        "room_number": 99,
        "description": "string",
        #"tables": [],
        "restaurant_id": get_restaurant_id
    }
    
    response = client.post("/api/v1/rooms", json=room_data, headers=headers)
    print(f' ESTO ES TUNA PRUEBA DE COMO ARMA EL RESPONSE ROOMS {response}')
    # Extraemos el id de la respuesta y lo devolvemos
    yield response.json()["data"]["_id"]



# Test para crear una Room en un Restaurante existente
def test_create_rooms(client, get_access_token, get_restaurant_id):
    """Prueba para el endpoint POST /v1/rooms."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    restaurant_id = get_restaurant_id
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    room_data = {
        "room_number": 1,
        "description": "string",
        #"tables": [],
        "restaurant_id": get_restaurant_id
    }
    
    response = client.post("/api/v1/rooms", json=room_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    # Extraemos el ID y lo almacenamos en la variable global
    global room_id_global  # Usar la variable global para almacenar el ID
    room_id_global = response.json()["data"]["_id"]
    print(f"Room ID: {room_id_global}")


# Test para crear una Room ya existente
def test_create_existing_room(client, get_access_token, get_restaurant_id):
    """Prueba para el endpoint POST /v1/rooms."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    restaurant_id = get_restaurant_id
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    room_data = {
        "room_number": 1,
        "description": "string",
        #"tables": [],
        "restaurant_id": get_restaurant_id
    }
    
    response = client.post("/api/v1/rooms", json=room_data, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT


# Test para crear una Room en un Restaurant inexistente
def test_create_room_with_invalid_restaurant_id(client, get_access_token):
    """Prueba para el endpoint POST /v1/rooms."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    room_data = {
        "room_number": 5,
        "description": "string",
        #"tables": [],
        "restaurant_id": "invalid_restaurant_id"
    }
    
    response = client.post("/api/v1/rooms", json=room_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Test para pedir las Rooms
def test_get_rooms(client, get_access_token):
    """Prueba para el endpoint GET /v1/rooms."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/rooms", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_room(response_data, True)
    

# Test para pedir una Room por id
def test_get_room_by_id(client, get_access_token):
    """Prueba para el endpoint GET /v1/rooms/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/api/v1/rooms/{room_id_global}", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_room(response_data)


# Test para modificar una Room por id
def test_patch_room_by_id(client, get_access_token, get_restaurant_id):
    """Prueba para el endpoint PATCH /v1/rooms/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    restaurant_id = get_restaurant_id
    # Encabezados con el token válido
    
    headers = {"Authorization": f"Bearer {token}"}
    
    room_data = {
        "room_number": 1,
        "description": "string_modified",
        #"tables": [],
        "restaurant_id": get_restaurant_id
    }

    response = client.patch(f"/api/v1/rooms/{room_id_global}", json=room_data, headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificamos que la modificación en "description" se haya efectuado correctamente
    check_modification = response.json()["data"]
    assert check_modification["description"] == "string_modified"


# Test para eliminar una Room por id
def test_delete_room_by_id(client, get_access_token):
    """Prueba para el endpoint DELETE /v1/rooms/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/rooms/{room_id_global}", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificamos que la eliminación del objeto Room se haya efectuado correctamente
    check_modification = response.json()["data"]
    assert check_modification["is_deleted"] == True
    for table in  check_modification["tables"]:
        assert table["is_deleted"] == True





# Funcion para verificar el cuerpo de las Rooms
def verificacion_data_room(response, data_is_list = False):
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
        assert "room_number" in room
        assert "description" in room
        #assert "tables" in room
        assert "restaurant_id" in room
        #assert isinstance(room["tables"], list)