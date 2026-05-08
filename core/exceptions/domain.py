from .base import DomainError
from starlette import status



class AlreadyExistsError(DomainError):
    def __init__(self, detail):
        self.detail = detail

    status_code = status.HTTP_409_CONFLICT


class NoResultFoundError(DomainError):
    def __init__(self, detail):
        self.detail = detail

    status_code = status.HTTP_404_NOT_FOUND

class TokenError(DomainError):
    def __init__(self, detail):
        self.detail = detail

    status_code = status.HTTP_401_UNAUTHORIZED