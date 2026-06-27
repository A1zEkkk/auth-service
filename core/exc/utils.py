from fastapi import Request
from fastapi.responses import JSONResponse

from .base import DomainError, ValidationError, TokenError, RefreshTokenError
from .domain.user import ResultNotFoundError, AlreadyExistsError
from core.exc.infrastructure.rabbit import NotificationDeliveryFailed


async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
    if isinstance(exc, ResultNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)}
        )

    if isinstance(exc, AlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)}
        )

    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": exc.__class__.__name__,
            "detail": str(exc)
        }
    )

async def token_exception_handler(
    request: Request,
    exc: TokenError,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        }
    )

async def refresh_token_exception_handler(
    request: Request,
    exc: RefreshTokenError,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        }
    )
