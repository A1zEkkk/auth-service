from core.exc.base import DomainError



class AlreadyExistsError(DomainError):
    pass

class ResultNotFoundError(DomainError):
    pass

