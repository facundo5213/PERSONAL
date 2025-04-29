import pytest
from fastapi import status
from core.config import settings
import os
from tests.test_user import get_access_token

restaurant_id_global = None

""" Función para crear un Restaurant y obtener el id.
Esta función la utilizarán todos los módulos para obtener 
el id que permite cubrir las dependencias
"""
@pytest.fixture(scope="session")
def get_restaurant_id(client, get_access_token):
    """Obtenemos el token y creamos el Restaurant"""
    # Primero logueamos y obtenemos el token
    #token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {get_access_token}"}

    restaurant_data = {
        "name": "Restaurante de prueba para uso de otros tests",
        "phone": "+39 123 4567 8910",
        "address": "Dirección de prueba",
        "comments": "Sin comentarios"
        #"employees": []
    }

    response = client.post("/api/v1/restaurants", json=restaurant_data, headers=headers)

    # Si el restaurante ya existe, recuperar su ID
    if response.status_code == 409:
        response = client.get("/api/v1/restaurants", headers=headers)
        for restaurant in response.json()["data"]:
            if restaurant["name"] == restaurant_data["name"]:
                yield restaurant["_id"]
    else:
        yield response.json()["data"]["_id"]
    # # Extraemos el id de la respuesta y lo devolvemos
    # yield response.json()["data"]["_id"]

# Test para crear un Restaurant
def test_create_restaurant(client, get_access_token):
    """Prueba para el endpoint POST /v1/restaurants."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    restaurant_data = {
        "name": "Restaurante de prueba",
        "phone": "+39 123 4567 8910",
        "address": "Dirección de prueba",
        "comments": "Sin comentarios"
        #"employees": []
    }
    
    response = client.post("/api/v1/restaurants", json=restaurant_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    # Extraemos el ID y lo almacenamos en la variable global
    global restaurant_id_global  # Usar la variable global para almacenar el ID
    restaurant_id_global = response.json()["data"]["_id"]
    print(f"Room ID: {restaurant_id_global}")


# Test para crear un Restaurant ya existente
def test_create_existing_restaurant(client, get_access_token):
    """Prueba para el endpoint POST /v1/restaurants."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    restaurant_data = {
        "name": "Restaurante de prueba",
        "phone": "+39 123 4567 8910",
        "address": "Dirección de prueba",
        "comments": "Sin comentarios"
        #"employees": []
    }
    
    response = client.post("/api/v1/restaurants", json=restaurant_data, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT

# Test para pedir los Restaurants
def test_get_restaurants(client, get_access_token):
    """Prueba para el endpoint GET /v1/restaurants."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/restaurants", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_restaurant(response_data, True)
    

# Test para pedir un Restaurant por id
def test_get_restaurant_by_id(client, get_access_token):
    """Prueba para el endpoint GET /v1/restaurants/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/api/v1/restaurants/{restaurant_id_global}", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    verificacion_data_restaurant(response_data)


# Test para modificar una Restaurant por id
def test_patch_restaurant_by_id(client, get_access_token):
    """Prueba para el endpoint PATCH /v1/restaurants/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    restaurant_data = {
        "name": "Restaurante de prueba",
        "phone": "+39 123 4567 8910 modified",
        "address": "Dirección de prueba modified",
        "comments": "Sin comentarios modified"
        #"employees": []
    }

    response = client.patch(f"/api/v1/restaurants/{restaurant_id_global}", json=restaurant_data, headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificamos que la modificación en "address" se haya efectuado correctamente
    check_modification = response.json()["data"]
    assert check_modification["address"] == "Dirección de prueba modified"


""" Test para eliminar un Restaurant por id con Rooms y/o Employees activos

Primero creamos un Employee asignado al restaurant_id_global e intentamos eliminar el restaurant esperando un 409
Eliminamos el Employee para liberar el Restaurant

Segundo creamos una Room asignada al restaurant_id_global e intentamos eliminar el restaurant esperando un 409
Eliminamos la Room para liberar el Restaurant
"""
def test_delete_restaurant_with_active_rooms_and_or_employees(client, get_access_token):
    """Prueba para el endpoint DELETE /v1/restaurants/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    """ Intentamos eliminar el Restaurant con un Employee asignado"""

    # Creamos un Employee asignado al Restaurant
    employee_input = {
        "identifier":100,
        "name":"John Doe",
        "role":"waiter",
        "comments":"string",  
        "phone":"string",    
        "address":"string",   
        "email":"user_employee@example.com",
        "restaurant_id": restaurant_id_global,  
        "emergency_contact":0,  
        "work_schedule":"morning",
        "assigned_tables": []
    }
    
    response = client.post("/api/v1/employees/", json=employee_input, headers=headers)
    employee = response.json()["data"]["_id"]
    
    # Intentamos eliminar el Restaurant
    response = client.delete(f"/api/v1/restaurants/{restaurant_id_global}", headers=headers)
    # Verificar que la respuesta sea HTTP 409 OK
    assert response.status_code == status.HTTP_409_CONFLICT

    # Eliminamos el Employee para liberar el restaurant para el próximo test de delete
    client.delete(f"api/v1/employees/{employee}", headers = headers)

    """ Intentamos eliminar el Restaurant con un Employee asignado"""

    # Creamos una Room asignada al Restaurant
    room_data = {
        "room_number": 200,
        "description": "string",
        "restaurant_id": restaurant_id_global
    }
    
    response = client.post("/api/v1/rooms", json=room_data, headers=headers)
    room = response.json()["data"]["_id"]

    # Intentamos eliminar el Restaurant
    response = client.delete(f"/api/v1/restaurants/{restaurant_id_global}", headers=headers)
    # Verificar que la respuesta sea HTTP 409 OK
    assert response.status_code == status.HTTP_409_CONFLICT

    # Eliminamos el Employee para liberar el restaurant para el próximo test de delete
    client.delete(f"/api/v1/rooms/{room}", headers=headers)


# Test para eliminar un Restaurant por id
def test_delete_restaurant_by_id(client, get_access_token):
    """Prueba para el endpoint DELETE /v1/restaurants/{id}."""
    # Primero logueamos y obtenemos el token
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/api/v1/restaurants/{restaurant_id_global}", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK




# Funcion para verificar el cuerpo de las Rooms
def verificacion_data_restaurant(response, data_is_list = False):
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
            restaurant = response["data"][0]
        else:
            restaurant = response["data"]
        
        assert "_id" in restaurant
        assert "created_at" in restaurant
        assert "updated_at" in restaurant
        assert "is_deleted" in restaurant
        assert "name" in restaurant
        assert "phone" in restaurant
        assert "address" in restaurant
        assert "comments" in restaurant
        # assert "employees" in restaurant
        # assert isinstance(restaurant["employees"], list)