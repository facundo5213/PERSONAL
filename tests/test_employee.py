import pytest
import os
from fastapi import status
from core.config import settings
from tests.test_rooms import get_rooms_id
from tests.test_restaurants import get_restaurant_id
from tests.test_user import get_access_token

employee_id_global = None 

@pytest.fixture(scope="session")
def get_employee_id(client, get_access_token, get_restaurant_id):
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    restaurant_id = get_restaurant_id #recibe id del restaurnte del test_restaurant
    employee_input = {
        "identifier":19,
        "name":"John Doe",
        "role":"waiter",
        "comments":"string",  
        "phone":"string",    
        "address":"string",   
        "email":"user_employee@example.com",
        "restaurant_id": restaurant_id,  
        "emergency_contact":0,  
        "work_schedule":"morning",
        "assigned_tables": []
    }
    
    response = client.post("/api/v1/employees/", json=employee_input, headers=headers)
    employee = response.json()["data"]["_id"]
    yield employee


def test_create_employee(client, get_access_token, get_restaurant_id):
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    restaurant_id = get_restaurant_id #recibe id del restaurnte del test_restaurant
    employee_input = {
        "identifier":1,
        "name":"John Doe",
        "role":"waiter",
        "comments":"string",  
        "phone":"string",    
        "address":"string",   
        "email":"user_employee@example.com",
        "restaurant_id": restaurant_id,  
        "emergency_contact":0,  
        "work_schedule":"morning",
        "assigned_tables": []
    }
    
    response = client.post("/api/v1/employees/", json=employee_input, headers=headers)
    assert response.status_code == 201
    employee = response.json()["data"]
    assert employee["restaurant_id"] == restaurant_id
    assert employee["role"] == "waiter"
    global employee_id_global  
    employee_id_global = response.json()["data"]["_id"]


def test_delete_employee(client, get_access_token, get_restaurant_id):
    # crea employee
    token = get_access_token
    # Encabezados con el token válido
    headers = {"Authorization": f"Bearer {token}"}
    # elimina employee
    response =  client.delete(f"api/v1/employees/{employee_id_global}", headers = headers)
    assert response.status_code == 200
