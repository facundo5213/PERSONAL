from pydantic import EmailStr, Field

from models.base import Base
from pydantic import BaseModel

from typing import List, Optional


#esto lo utilizo para la generacion de un nuevo usuario
class UsersModel(Base):
    _collection_name = "users"

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    rol: str
    restaurantes: str



#esto lo utilizo para cuando hago un get, excluir el campo password
class UserResponseModel(Base):
    _collection_name = "users"

    first_name: str
    last_name: str
    email: EmailStr
    rol: str
    restaurantes: str

class LoginData(BaseModel):
    username: str
    password: str



