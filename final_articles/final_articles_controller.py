from fastapi import APIRouter, Request, Response, status, Depends
from core.db import get_mongo_db

from api.final_articles.final_articles_service import FinalArticles as Service

from models.final_articles import FinalArticlesModel  as Model
from models.users import UserResponseModel

from schemas.response import ResponseBase
from schemas.final_articles import FinalArticlesInput as Input

from utils.exceptions.response_handler import response_handler
from utils.presentation.response import ApiResponse
from utils.oauth.auth import get_user_current


ITEM = "final_articles" 

##################################################################################################

final_articles_router: APIRouter = APIRouter(prefix="/v1/final_articles")

@final_articles_router.post(
    "",
    tags=["Final Articles"],
    description=f"Create {ITEM}"
)
@response_handler(response_status=status.HTTP_201_CREATED)
async def create(
        request: Request,
        response: Response,
        _input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: UserResponseModel = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init create {ITEM}")
    service = Service(api_response, main_db) ##
    item_db = await service.add(_input, token.restaurantes) ##
    api_response.logger.info(f"Finish create {ITEM}: {item_db}") ##
    return item_db

@final_articles_router.get(
    "",
    tags=["Final Articles"],
    description=f"Get {ITEM}s"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get(
    request:Request,
    response:Response,
    api_response=Depends(ApiResponse),
    main_db=Depends(get_mongo_db),
    token: str = Depends(get_user_current),
) -> ResponseBase[list[Model]]:
    api_response.logger.info(f"Init get all {ITEM}")
    service = Service(api_response, main_db)
    items_db = await service.get()
    api_response.logger.info(f"Finish get {ITEM}: {items_db}")
    return items_db

###hasta aca
@final_articles_router.get(
    "/{final_articles_id}",
    tags=["Final Articles"],
    description=f"Get {ITEM} by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def get_by_id(
        request: Request,
        response: Response,
        final_articles_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init get {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.get_by_id(final_articles_id)
    api_response.logger.info(f"Finish get {ITEM}: {item_db}")
    return item_db

@final_articles_router.patch(
    "/{final_articles_id}",
    tags=["Final Articles"],
    description=f"Modify {ITEM} by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def modify_by_id(
        request: Request,
        response: Response,
        final_articles_id: str,
        modify_input: Input,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init modify {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.change(final_articles_id, modify_input)
    api_response.logger.info(f"Finish modify {ITEM}: {item_db}")
    return item_db



@final_articles_router.delete(
    "/{final_articles_id}",
    tags=["Final Articles"],
    description=f"Delete {ITEM} by id"
)
@response_handler(response_status=status.HTTP_200_OK)
async def delete_by_id(
        request: Request,
        response: Response,
        final_articles_id: str,
        api_response=Depends(ApiResponse),
        main_db=Depends(get_mongo_db),
        token: str = Depends(get_user_current),
) -> ResponseBase[Model]:
    api_response.logger.info(f"Init delete {ITEM}")
    service = Service(api_response, main_db)
    item_db = await service.delete_by_id(final_articles_id)
    api_response.logger.info(f"Finish delete {ITEM}: {item_db}")
    return item_db
