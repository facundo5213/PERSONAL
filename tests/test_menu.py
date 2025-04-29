
import pytest
from fastapi import status
from core.config import settings
import os
from tests.test_user import get_access_token
from tests.test_rooms import get_rooms_id



# Test para crear un menu
def test_create_menu(client, get_access_token):
    """Prueba para el endpoint POST /v1/tables."""
    
    headers = {"Authorization": f"Bearer {get_access_token}"}
    table_data = {
        "nombre": "string",
        "descripcion": "string",
        "precio": 0
        }
    
    response = client.post("/api/v1/menus", json=table_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    # Extraemos el ID y lo almacenamos en la variable global
    global menu_id_global
    menu_id_global = response.json()["data"]["_id"]
    

#test para traer los menu
def test_get_menu(client, get_access_token):
    """Prueba para el endpoint POST /v1/tables."""
    global menu_id_global

    headers = {"Authorization": f"Bearer {get_access_token}"}

    response = client.get("/api/v1/menus", headers=headers)
    assert response.status_code == status.HTTP_200_OK

def test_patch_menu(client, get_access_token):
    global menu_id_global  # Declarar como global
    headers = {"Authorization": f"Bearer {get_access_token}"}
    table_data = {
        "nombre": "string",
        "descripcion": "string",
        "precio": 10
    }

    response = client.patch(f"/api/v1/menus/{menu_id_global}", json=table_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    # Actualizar el ID si es necesario
    menu_id_global = response.json()["data"]["_id"]

def test_delete_menu(client, get_access_token):
    global menu_id_global  # Declarar como global
    headers = {"Authorization": f"Bearer {get_access_token}"}
    table_data = {
        "nombre": "string",
        "descripcion": "string",
        "precio": 0
        }
    
    response = client.post("/api/v1/menus", json=table_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    # Extraemos el ID y lo almacenamos en la variable global
    menu_id_del = response.json()["data"]["_id"]
    print(menu_id_del)

    response = client.delete(f"/api/v1/menus/{menu_id_del}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

