import pytest
from fastapi import status
from schemas.users import UsersInput
from models.users import UserResponseModel
from core.config import settings
import os
from dotenv import load_dotenv
from utils.oauth.auth import get_user_current

load_dotenv()

""" Función para registrar y obtener el token logueando.
Esta función la utilizarán todos los módulos para obtener 
el usuario que permite cubrir las dependencias
"""
@pytest.fixture(scope="session")
def get_access_token(client):
    """Creamos el usuario"""
    user_data = {
        "first_name": "string",
        "last_name": "string",
        "email": "user_for_fixture@example.com",
        "password": "string",
        "rol": "string",
        "restaurantes": []
    }
    
    client.post("/api/v1/users", json=user_data)

    """Obtiene el token de acceso haciendo login."""
    user_data = {
        "username": "user_for_fixture@example.com",  # Datos del usuario de prueba
        "password": "string"
    }
    # Solicita el token
    response = client.post("/api/v1/token", json=user_data)
    
    # Extrae el token de la respuesta
    response_data = response.json()
    yield response_data["access_token"]

# Función para obtener el token
def get_access_token_fail(client):
    """Obtiene el token de acceso haciendo login con credenciales incorrectas."""
    user_data = {
        "username": "us@example.com",  # Datos del usuario de prueba
        "password": "string"
    }
    # Solicita el token
    response = client.post("/api/v1/token", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.fixture(scope="session")
def create_user_and_get_id(client):
    """Crea un usuario y retorna su ID."""
    user_data = {
        "first_name": "usuario_test2",
        "last_name": "string",
        "email": "usuario_test2@example.com",  
        "password": "string",
        "rol": "string",
        "restaurantes": []
    }
    
    # Realiza la solicitud POST para crear el usuario
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    
    # Obtiene y retorna el ID del usuario creado
    response_data = response.json()
    user_id = response_data["data"]["_id"]

    return user_id

#testeo de creacion de usuario POST /api/v1/users
def test_create_user(client):
    """Prueba para el endpoint POST /v1/users."""
    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    user_data = {
        "first_name": "string",
        "last_name": "string",
        "email": "usdfsdfsdfg@example.com",
        "password": "string",
        "rol": "string",
        "restaurantes": []
    }
    
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_200_OK

#testeo de crear un usuario sin mail.
def test_create_user_without_email(client):
    """Prueba para el endpoint POST /v1/users."""
    print(f"Conectado a la base de datos: {settings.MAIN_DB_NAME}")
    env_value = os.getenv("ENV")
    print(f"Valor de ENV: {env_value}")
    user_data = {
        "first_name": "string",
        "last_name": "string",
        "password": "string",
        "rol": "string",
        "restaurantes": []
    }
    
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Accede al mensaje de error específico en la respuesta.
    error_detail = response.json()["detail"]

    # Asegura que haya al menos un error y que esté relacionado con el campo 'email'.
    assert len(error_detail) > 0
    assert error_detail[0]["loc"] == ["body", "email"]  # Verifica que el error está en el campo 'email'.
    assert error_detail[0]["msg"] == "Field required"

#testeo de login con credenciales correctas
def test_login_user_invalid_credentials(client):
    """Prueba para el endpoint POST /v1/token."""
    user_data = {
        "username": "usdfsdfsdfg@example.com",
        "password": "sjnordunudustiong"
    }
    response = client.post("/api/v1/token", json=user_data)
    # Verificar que la respuesta sea HTTP 401
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_user_fail(client):
    """Prueba para el endpoint POST /v1/token."""
    user_data = {
        "username": "us@example.com",
        "password": "string"
    }
    response = client.post("/api/v1/token", json=user_data)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_400_BAD_REQUEST

#testeo con credenciales correctas
def test_get_users_with_valid_token(client, get_access_token):
    """Prueba para el endpoint GET /v1/users con un token válido."""
    # Obtener token válido
    token = get_access_token
    
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/users", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    print(response.json())  # Imprime los datos de la respuesta para depuración

#testeo con credenciales incorrectas
def test_get_users_with_valid_token_fail(client):
    """Prueba para el endpoint GET /v1/users con un token  invalido válido."""
    # Obtener token válido
    token = get_access_token_fail(client)
    
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/users", headers=headers)
    
    # Verificar que la respuesta sea HTTP 401 unauthorized
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    print(response.json())  # Imprime los datos de la respuesta para depuración

#testeo de traer usuarios de usuario POST /api/v1/users
def test_get_user(client, get_access_token):
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    
    # Hacer una solicitud GET al endpoint
    response = client.get("/api/v1/users", headers=headers)
    
    # Verificar que la respuesta sea HTTP 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que el cuerpo de la respuesta tenga la estructura esperada
    response_data = response.json()
    assert "status_code" in response_data
    assert "data" in response_data
    assert isinstance(response_data["data"], list)
    assert "errors" in response_data
    assert "request_id" in response_data

    # Verificar que los campos dentro de "data" estén presentes y correctos
    if response_data["data"]:  # Solo si hay usuarios en la respuesta
        user = response_data["data"][0]
        assert "_id" in user
        assert "created_at" in user
        assert "updated_at" in user
        assert "is_deleted" in user
        assert "first_name" in user
        assert "last_name" in user
        assert "email" in user
        assert "rol" in user
        assert "restaurantes" in user
        assert isinstance(user["restaurantes"], list)

#testeo de traer un usuario especifico por id GET /api/v1/users/{user_id}
def test_get_user_by_id(client, get_access_token, create_user_and_get_id):
    token = get_access_token
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = create_user_and_get_id  
    print(f"User ID para el GET /users/{user_id}: {user_id}")  

    response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    # Verificaciones en la respuesta
    assert "status_code" in response_data
    assert "data" in response_data
    assert response_data["data"]["_id"] == user_id
    assert "errors" in response_data
    assert "request_id" in response_data

#testeo de traer un usuario que no existe por id GET /api/v1/users/{user_id}
def test_get_user_by_id_nonexistent(client, get_access_token, create_user_and_get_id):
    token = get_access_token
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = 'usuarioquenoexiste'
    print(f"User ID para el GET /users/{user_id}: {user_id}")  

    response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    
    # Verificaciones en la respuesta
    assert "status_code" in response_data
    assert "data" in response_data
    assert "errors" in response_data
    assert "request_id" in response_data

#testeo para modificar el rol de un usuario PATCH /api/v1/users/{user_id}
def test_update_user(client, get_access_token, create_user_and_get_id):
    token = get_access_token
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = create_user_and_get_id  
    print(f"User ID para el GET /users/{user_id}: {user_id}")  
    user_data = {
        "rol": "Administrador",
    }


    response = client.patch(f"/api/v1/users/{user_id}", headers=headers,json=user_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "data" in response_data
    assert response_data["data"]["rol"] == 'Administrador'

#testeo para eliminar un usuario por id DELETE /api/v1/users/{user_id}
def test_delete_user(client, get_access_token, create_user_and_get_id):
    token = get_access_token
    headers = {"Authorization": f"Bearer {token}"}
    
    user_id = create_user_and_get_id 
    
    response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    
    # Verificaciones en la respuesta
    assert "status_code" in response_data
    assert response_data["status_code"] == status.HTTP_200_OK
    assert "data" in response_data
    assert response_data["data"] is None  
    assert "errors" in response_data
    assert "request_id" in response_data
