import logging
from functools import wraps
from core.schemas.http import HTTPError

logger = logging.getLogger(__name__)


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpException as e:
            logger.error(f"HttpException: {e}")
            return e.to_http_error()
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
            return HTTPError(
                status_code=500,
                details=f"Internal server error"
            ).to_dict()

    return wrapper


class HttpException(Exception):
    """Base class for HTTP exceptions"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def to_http_error(self) -> HTTPError:
        """Convert to HTTP error"""
        return HTTPError(status_code=self.status_code, details=self.message).to_dict()
