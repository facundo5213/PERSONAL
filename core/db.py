# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# from core.config import settings


# def get_mongo_db() -> AsyncIOMotorDatabase:
#     client = AsyncIOMotorClient(str(settings.mongo_connection_string))
#     return client[settings.MAIN_DB_NAME]

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import settings

# Crear una instancia global de cliente
client = AsyncIOMotorClient(str(settings.mongo_connection_string))

def get_mongo_client() -> AsyncIOMotorClient:
    return client

def get_mongo_db() -> AsyncIOMotorDatabase:
    return client[settings.MAIN_DB_NAME]
