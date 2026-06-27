

class DomainError(Exception):
    pass

class ValidationError(Exception):
    pass

class TokenError(Exception):
    pass

class RefreshTokenError(Exception): #Доменная для бд
    pass

class InfrastructureRabbitError(Exception):
    pass