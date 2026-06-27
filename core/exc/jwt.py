from .base import TokenError


class TokenSignatureError(TokenError):
    pass

class TokenExpiredError(TokenError):
    pass

class TokenClaimError(TokenError):
    pass

class TokenDecodeError(TokenError):
    pass

class TokenInvalidError(TokenError):
    pass
