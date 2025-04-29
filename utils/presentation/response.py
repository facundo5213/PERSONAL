from typing import Any

from starlette import status

from schemas.errors import ErrorResponse
from schemas.response import ResponseBase
from utils.logging.logging import Logging
from utils.presentation.errors import DefaultException, _BaseException


class ApiResponse:
    def __init__(self):
        self._status_code: int = status.HTTP_400_BAD_REQUEST
        self._data = None
        self._errors = []
        self._logger = Logging()

    @property
    def data(self):
        return self._data

    @property
    def errors(self):
        return self._errors

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = value

    @property
    def logger(self):
        return self._logger

    def response(self, response_model=ResponseBase):
        response = response_model(
            status_code=self._status_code,
            data=self._data,
            errors=self._errors,
            request_id=self._logger.request_id
        ).model_dump()

        return response

    @property
    def request_id(self):
        return self._logger.request_id


    def add_error(self, error: _BaseException):
        error = ErrorResponse(**error.error_schema)
        self._errors.append(error.model_dump())

    def set_result(self, result: Any):
        self._data = result

    def process_general_exception(self, e: Exception):
        self._logger.error(f'Unexpected Error! {type(e)} {str(e)}')
        self.add_error(DefaultException(str(e)))
