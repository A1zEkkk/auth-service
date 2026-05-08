class MainException(Exception):
    pass

class DomainError(MainException):
    pass

class ValidationError(MainException):
    pass