from fastapi import APIRouter, Request, Response, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError
import os

from utils.exceptions.response_handler import response_handler

from core.db import get_mongo_db
from utils.presentation.response import ApiResponse
from api.users.users_service import UsersService
from utils.oauth.oauth import oauth2_scheme
from schemas.users import LoginData

auth_router = APIRouter(prefix="/v1/token")






# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = "HS256"

def create_token(data: dict, time_expire: Union[datetime, None]=None):
    data_copy = data.copy()
    
    if time_expire is not None:
        # Si se pasa un tiempo de expiración, agregar la clave 'exp' con el tiempo de expiración
        expires = datetime.utcnow() + time_expire
        data_copy.update({"exp": expires})
        
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

async def get_user_current(token: str = Depends(oauth2_scheme), api_response=Depends(ApiResponse), main_db=Depends(get_mongo_db)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token_decode.get("id_")
        if user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    user_service = UsersService(api_response, main_db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    return user

@auth_router.post(
    "",
    tags=["token"]
)
async def login(
    login_data: LoginData,  # Argumentos sin valor por defecto primero
    request: Request,
    response: Response,
    api_response=Depends(ApiResponse),
    main_db=Depends(get_mongo_db)
):
    api_response.logger.info("Init token user")
    user_service = UsersService(api_response, main_db)
    user = await user_service.get_user_by_email(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    
    access_token_jwt = create_token({"sub": user['email'], "id_": user['_id']})
    api_response.logger.info(f"Finish token user: {user['_id']}")

    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

@auth_router.post(
    "/form",
    tags=["token/form"]
)
async def login_form(
    login_data: OAuth2PasswordRequestForm = Depends(), # Form para hacer login en la docs de swagger (Authorize)
    #request: Request,
    #response: Response,
    api_response=Depends(ApiResponse),
    main_db=Depends(get_mongo_db)
):
    api_response.logger.info("Init token user")
    user_service = UsersService(api_response, main_db)
    user = await user_service.get_user_by_email(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})
    

    access_token_jwt = create_token({"sub": user['email'], "id_": user['_id']})
    
    api_response.logger.info(f"Finish token user: {user['_id']}")

    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }