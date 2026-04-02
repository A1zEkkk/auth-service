from core.exceptions.base import CustomException
from core.enums.exception_status import ExceptionStatus
from core.enums.status_type import StatusType


class TokenNotFound(CustomException):
    status = StatusType.ERROR.value
    status_type = ExceptionStatus.TOKEN_EXPIRED.name
    message = ExceptionStatus.UNAUTHORIZED.message
    _status_code = ExceptionStatus.UNAUTHORIZED.status_code