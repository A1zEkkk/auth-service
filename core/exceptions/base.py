from starlette import status


class MainException(Exception):
    pass


class UserAlreadyExistsError(MainException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"

class InvalidPasswordError(MainException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Password is incorrect"

class UserNoResultFoundError(MainException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User doesn't exist"

class IncorrectPasswordLengthError(MainException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Password is incorrect"

class IncorrectPasswordRuleError(MainException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Password is incorrect"

class InvalidPhoneNumberError(MainException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Password is incorrect"