from functools import wraps

from fastapi import Request, Response
from pydantic import ValidationError
from starlette import status

from utils.presentation.errors import NotFoundException, MissingParameterException, ThirdPartyException, \
    AlreadyExistsException, InvalidParameterException, ForbiddenException, AuthenticationException, DefaultException
from utils.presentation.response import ApiResponse


def response_handler(response_status: status = status.HTTP_200_OK):
    def wrapper(func):
        @wraps(func)
        async def wrapped_func(request: Request, response: Response, *args, **kwargs):
            api_response: ApiResponse = kwargs.get("api_response")
            api_response.status_code = response_status
            response_model = None
            try:
                response_model = func.__annotations__.get("return")
                result = await func(request, response, *args, **kwargs)
                if result:
                    api_response.set_result(result)
            except NotFoundException as err:
                api_response.logger.error(err)
                api_response.add_error(err)
                api_response.status_code = status.HTTP_404_NOT_FOUND
            except (MissingParameterException, ThirdPartyException,
                    InvalidParameterException) as err:
                api_response.logger.error(err)
                api_response.add_error(err)
                api_response.status_code = status.HTTP_400_BAD_REQUEST
            except ForbiddenException as err:
                api_response.logger.error(err)
                api_response.add_error(err)
                api_response.status_code = status.HTTP_403_FORBIDDEN
            except AuthenticationException as err:
                api_response.logger.error(err)
                api_response.add_error(err)
                api_response.status_code = status.HTTP_401_UNAUTHORIZED

            except AlreadyExistsException as err:
                api_response.logger.error(err)
                api_response.add_error(err)
                api_response.status_code = status.HTTP_409_CONFLICT

            except Exception as e:
                api_response.process_general_exception(e)
                api_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            try:
                response_data = api_response.response(response_model)
            except ValidationError as err:
                api_response.set_result(None)
                api_response.add_error(DefaultException("Errors in the response model"))
                api_response.logger.error(f"Error in response model: {err}")
                response_data = api_response.response()

            response.status_code = api_response.status_code

            return response_data

        return wrapped_func

    return wrapper
