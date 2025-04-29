
import pytest
from fastapi import status
from core.config import settings
import os
from tests.test_user import get_access_token
from tests.test_rooms import get_rooms_id
from tests.test_restaurants import get_restaurant_id
from tests.test_employee import get_employee_id


table_id_global = None 
#rooms_id_fixture = get_rooms_id


""" Función para crear un Restaurant y obtener el id.
Esta función la utilizarán todos los módulos para obtener 
el id que permite cubrir las dependencias
"""
@pytest.fixture(scope="session")
def get_tables_id(client, get_access_token, get_rooms_id):
        headers = {"Authorization": f"Bearer {get_access_token}"}
        table_data = {
                "table_number": 10,
                "capacity": 4,
                "status": "string",
                "orders": [],
                "assigned_employee": "string",
                "room_id": get_rooms_id,
                "assigned_at": "string"
        }
        response = client.post("/api/v1/tables", json=table_data, headers=headers)
        # Extraemos el id de la respuesta y lo devolvemos
        yield response.json()["data"]["_id"]


# Test para crear una Table en una Room de un Restaurant
def test_create_table(client, get_access_token,  get_rooms_id):
        """Prueba para el endpoint POST /v1/tables."""
        headers = {"Authorization": f"Bearer {get_access_token}"}
        table_data = {
                "table_number": 1,
                "capacity": 4,
                "status": "string",
                "orders": [],
                "assigned_employee": "string",
                "room_id": get_rooms_id,
                "assigned_at": "string"
        }
        
        response = client.post("/api/v1/tables", json=table_data, headers=headers)
        assert response.status_code == status.HTTP_200_OK

        # Extraemos el ID y lo almacenamos en la variable global
        global table_id_global
        table_id_global = response.json()["data"]["_id"]
        response_data = response.json()["data"]
        assert response_data["table_number"] == table_data["table_number"]
        assert response_data["capacity"] == table_data["capacity"]
        assert response_data["room_id"] == get_rooms_id



# Test para crear una Room ya existente
def test_create_existing_room(client, get_access_token,  get_rooms_id):
        """Prueba para el endpoint POST /v1/rooms."""

        headers = {"Authorization": f"Bearer {get_access_token}"}
        table_data = {
                "table_number": 1,
                "capacity": 4,
                "status": "string",
                "orders": [],
                "assigned_employee": "string",
                "room_id": get_rooms_id,
                "assigned_at": "string"
        }
        
        response = client.post("/api/v1/tables", json=table_data, headers=headers)
        assert response.status_code == status.HTTP_409_CONFLICT
        
def test_get_tables_by_id(client, get_access_token):
        headers = {"Authorization": f"Bearer {get_access_token}"} 
        global table_id_global
        response = client.get(f"/api/v1/tables/{table_id_global}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        
def test_assign_tables(client, get_access_token, get_employee_id):
        employee_id =  get_employee_id
        #voy a buscar el identificador del empleado
        headers = {"Authorization": f"Bearer {get_access_token}"} 
        
        response = client.get(f"/api/v1/employees/{employee_id}", headers=headers)
        identifier = response.json()["data"]["identifier"]
        
        data_employee = {
                "identifier" : identifier
        }
        response = client.patch(f"/api/v1/tables/{table_id_global}/assign", json=data_employee,headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["assigned_employee"] == employee_id


def test_unassign_tables(client, get_access_token, get_employee_id):
        employee_id =  get_employee_id
        #voy a buscar el identificador del empleado
        headers = {"Authorization": f"Bearer {get_access_token}"} 
        
        response = client.get(f"/api/v1/employees/{employee_id}", headers=headers)
        identifier = response.json()["data"]["identifier"]
        
        data_employee = {
                "identifier" : identifier
        }
        response = client.patch(f"/api/v1/tables/{table_id_global}/unassign", json=data_employee,headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["assigned_employee"] == ''


def test_close_tables(client, get_access_token):
        headers = {"Authorization": f"Bearer {get_access_token}"} 
        
        response = client.patch(f"/api/v1/tables/{table_id_global}/close",headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["status"] == "close"


def test_available_tables(client, get_access_token):
        headers = {"Authorization": f"Bearer {get_access_token}"} 
        
        response = client.patch(f"/api/v1/tables/{table_id_global}/available",headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["status"] == "available"


def test_patch_tables_by_id(client, get_access_token,  get_rooms_id):
        headers = {"Authorization": f"Bearer {get_access_token}"} 

        table_data = {
                "capacity": 40,
        }
        response = client.patch(f"/api/v1/tables/{table_id_global}", json=table_data ,headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["capacity"] == 40
        

def test_delete_tables_by_id(client, get_access_token):
        headers = {"Authorization": f"Bearer {get_access_token}"} 

        response = client.delete(f"/api/v1/tables/{table_id_global}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
