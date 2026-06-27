from .base import ValidationError

class InvalidLengthError(ValidationError):
    pass

class InvalidSymbolError(ValidationError):
    pass

class InvalidPasswordError(ValidationError):
    pass