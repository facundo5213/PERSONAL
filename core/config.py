from fastapi.routing import APIRoute
from pydantic import computed_field, MongoDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

def load_env_file():
    env = os.getenv("ENV", "local")
    if env == "test":
        load_dotenv(".env.test")
    else:
        load_dotenv(".env")

load_env_file()

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    API_STR: str = "/api"
    PROJECT_NAME: str
    ENV: str
    DOMAIN: str
    MAIN_DB_NAME: str
    APP_VERSION: str = "1.0.0"  # Versión base

    MONGO_USER: str | None = None
    MONGO_PASSWORD: str | None = None
    MONGO_HOST: str
    MONGO_PORT: int = 27017  # Puerto por defecto para MongoDB



    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENV == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

class LocalConfig(BaseConfig):
    ENV: str = "local"
    APP_VERSION: str = "1.0.0-dev"  # Subversión para desarrollo

    @computed_field
    @property
    def mongo_connection_string(self) -> MongoDsn:
        return MongoDsn.build(
            scheme="mongodb",
            username=self.MONGO_USER,
            password=self.MONGO_PASSWORD,
            host=self.MONGO_HOST,
            port=self.MONGO_PORT,
            path=self.MAIN_DB_NAME,
        )

class ProductionConfig(BaseConfig):
    ENV: str = "production"
    APP_VERSION: str = "1.0.0"  # Versión de producción

    @computed_field
    @property
    def mongo_connection_string(self) -> MongoDsn:
        return MongoDsn.build(
            scheme="mongodb+srv",
            username=self.MONGO_USER,
            password=self.MONGO_PASSWORD,
            host=self.MONGO_HOST,
            path=self.MAIN_DB_NAME,
        )

class ConfigForTesting(BaseConfig):
    ENV: str = "test"
    APP_VERSION: str = "1.0.0-dev"  # Subversión para desarrollo
    MAIN_DB_NAME: str = "test_db"

    @computed_field
    @property
    def mongo_connection_string(self) -> MongoDsn:
        return MongoDsn.build(
            scheme="mongodb",
            username=self.MONGO_USER,
            password=self.MONGO_PASSWORD,
            host=self.MONGO_HOST,
            port=self.MONGO_PORT,
            path=self.MAIN_DB_NAME,
        )




# Función para obtener la configuración correcta según el entorno
def get_settings() -> BaseConfig:
    env = os.getenv("ENV", "local") # Obtiene la variable de entorno ENV
    print(f"Loading settings for environment: {env}")
    if env == "local":
        return LocalConfig()
    elif env == "production":
        return ProductionConfig()
    elif env == "test":
        return ConfigForTesting()
    else:
        raise ValueError(f"Invalid ENV value: {env}")

# Inicializar la configuración según el entorno
settings = get_settings()
print(f"Configuración actual: {settings.MAIN_DB_NAME}")