# import pytest
# from fastapi.testclient import TestClient
# from dotenv import load_dotenv
# import os

# # Cargar el archivo .env.test antes que cualquier otro componente
# load_dotenv(".env.test", override=True)  # Sobreescribe cualquier variable de entorno existente

# # Imprimir para verificar que se está cargando el archivo correcto
# print(f"MAIN_DB_NAME from .env.test: {os.getenv('MAIN_DB_NAME')}")
# print(f"ENV from .env.test: {os.getenv('ENV')}")

# from main import app  # Importar después de cargar las variables de entorno

# @pytest.fixture(scope="session", autouse=True)
# def load_test_env():
#     """Fixture para asegurarse de que .env.test se cargue correctamente."""
#     assert os.getenv('MAIN_DB_NAME') == "test_database", "MAIN_DB_NAME no coincide con el entorno de prueba"

# @pytest.fixture
# def client():
#     """Fixture para crear un cliente de prueba."""
#     return TestClient(app)


import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar el archivo .env.test antes que cualquier otro componente
load_dotenv(".env.test", override=True)  # Sobreescribe cualquier variable de entorno existente

# Imprimir para verificar que se está cargando el archivo correcto
print(f"MAIN_DB_NAME from .env.test: {os.getenv('MAIN_DB_NAME')}")
print(f"ENV from .env.test: {os.getenv('ENV')}")

from main import app  # Importar después de cargar las variables de entorno

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Fixture para asegurarse de que .env.test se cargue correctamente."""
    assert os.getenv('MAIN_DB_NAME') == "test_database", "MAIN_DB_NAME no coincide con el entorno de prueba"

@pytest.fixture(scope="session")
def client():
    """Fixture para crear un cliente de prueba."""
    return TestClient(app)

@pytest.fixture(scope="session")
def db_client():
    client = MongoClient()
    yield client
    client.close()  # Cerrar la conexión después de las pruebas

@pytest.fixture(scope="session", autouse=True)
def clear_db(db_client):
    """Limpia la base de datos después de cada prueba."""
    db = db_client.get_database(os.getenv('MAIN_DB_NAME'))  # Conexión a la base de datos de prueba

    # Eliminar todas las colecciones de la base de datos
    print(f"Inicio de limpieza de la base de datos {os.getenv('MAIN_DB_NAME')}")
    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)
        print(f"Colección: '{collection_name}' eliminada")

    yield

    