from fastapi.responses import JSONResponse
from fastapi import Request
from .base import MainException

async def app_exception_handler(request: Request, exc: MainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )