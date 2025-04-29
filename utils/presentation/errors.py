class _BaseException(Exception):
    def __init__(self, error: str, description: str, message: str):
        self.error = error
        self.description = description
        self.message = message

    @property
    def error_schema(self):
        return {
            "error": self.error,
            "description": self.description,
            "message": self.message,
        }

    def __str__(self):
        return f"Error: {self.error}: {self.description} - message: {self.message}"


class _Exception(_BaseException):
    def __init__(self, message: str):
        super().__init__(self.error, self.description, message)


class AlreadyExistsException(_Exception):
    error = "ALREADY_EXISTS"
    description = "The resource already exists."


class AuthenticationException(_Exception):
    error = "UNAUTHORIZED"
    description = "Invalid authentication credentials."


class ForbiddenException(_Exception):
    error = "FORBIDDEN"
    description = "Permission denied."


class InvalidParameterException(_Exception):
    error = "INVALID_PARAMETER"
    description = "Invalid parameter value."


class MissingParameterException(_Exception):
    error = "MISSING_PARAMETER"
    description = "The request is missing a required parameter."


class NotFoundException(_Exception):
    error = "NOT_FOUND"
    description = "The specified resource was not found."


class ThirdPartyException(_Exception):
    error = "THIRD_PARTY_ERROR"
    description = "An error occurred while communicating with a third party."


class DefaultException(_Exception):
    error = "UNEXPECTED_ERROR"
    description = "Unexpected Error."
    message = "An unexpected error occurred. Please try again or contact support and provide the request id."

    def __init__(self, message: str = None):
        if message is None:
            message = self.message
        super().__init__(message)


class TransactionException(_Exception):
    error = "TRANSACTION_ERROR"
    description = "An error occurred during the database transaction."

    def __init__(self, message: str = "A transaction-related error occurred."):
        super().__init__(message)