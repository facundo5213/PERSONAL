import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from colorama import Fore, init

from api.router import ACTIVE_ROUTERS
from core.config import settings, custom_generate_unique_id

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in ACTIVE_ROUTERS:
    app.include_router(router, prefix=settings.API_STR)
"""
if __name__ == "__main__":
    logger.info(Fore.YELLOW + "Starting the FastAPI server...")
    if settings.ENV == "local":
        logger.info(Fore.GREEN + f"Running in local environment with version {settings.APP_VERSION}")
    else:
        logger.info(Fore.GREEN + f"Running in production environment with version {settings.APP_VERSION}")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    
