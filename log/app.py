import logging
import logging.config
import sys
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware



import logging
import logging.config
import sys
import json
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar


# --- request_id context ---
request_id_ctx = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
        }
        return json.dumps(log_record, ensure_ascii=False)


def setup_logging(level: str = "INFO"):
    config = {
        "version": 1,
        "disable_existing_loggers": False,

        "filters": {
            "request_id": {
                "()": RequestIdFilter,
            }
        },

        "formatters": {
            "json": {
                "()": JsonFormatter,
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json",
                "filters": ["request_id"],
            }
        },

        "loggers": {
            "app": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },

            "uvicorn": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": level,
                "propagate": False,
            },
        },

        "root": {
            "handlers": ["console"],
            "level": level,
        },
    }

    logging.config.dictConfig(config)


logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)

        start_time = time.time()

        logger.info(
            f"Request {request.method} {request.url.path}"
        )

        try:
            response = await call_next(request)
            return response

        except Exception as e:
            logger.exception(
                f"Error {request.method} {request.url.path}: {str(e)}"
            )
            raise

        finally:
            process_time = (time.time() - start_time) * 1000

            logger.info(
                f"Response {request.method} {request.url.path} "
                f"status={getattr(locals().get('response', None), 'status_code', 'ERR')} "
                f"time={process_time:.2f}ms"
            )