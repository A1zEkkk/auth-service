from starlette import status
from .base import MainException

class AuthDataError(MainException):
    def __init__(self, detail):
        self.detail = detail

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
