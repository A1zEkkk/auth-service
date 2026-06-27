from core.exc.base import RefreshTokenError


class RefreshTokenNotFoundError(RefreshTokenError):
    pass

class RefreshTokenExpiredError(RefreshTokenError):
    pass

class RefreshTokenRevokedError(RefreshTokenError):
    pass