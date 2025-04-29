from fastapi import APIRouter, Request, Response, status

health_router: APIRouter = APIRouter(prefix="/v1/health")


@health_router.get("", tags=["Health"], response_model=dict, status_code=status.HTTP_200_OK)
async def get_health(request: Request, response: Response) -> dict:
    return {"status": "ok"}


@health_router.post("", tags=["Health"], response_model=dict, status_code=status.HTTP_200_OK)
async def post_health(request: Request, response: Response, health_input: dict) -> dict:
    return health_input
