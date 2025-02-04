from flask import jsonify
from pydantic import ValidationError
from functools import wraps
import structlog
from typing import Callable, Any

logger = structlog.get_logger(__name__)

class APIError(Exception):
    """Base API Error class"""
    def __init__(self, message: str, status_code: int = 400, payload: Any = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

def handle_api_error(error: APIError):
    """Handler for API errors"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def error_handler(f: Callable) -> Callable:
    """Decorator for handling errors in route handlers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.error("validation_error", errors=str(e))
            return jsonify({
                'status': 'error',
                'message': 'Validation error',
                'errors': e.errors()
            }), 400
        except APIError as e:
            logger.error(
                "api_error",
                status_code=e.status_code,
                message=e.message
            )
            return handle_api_error(e)
        except Exception as e:
            logger.error(
                "unexpected_error",
                error=str(e),
                exc_info=True
            )
            return jsonify({
                'status': 'error',
                'message': 'An unexpected error occurred'
            }), 500
    return decorated_function

# Common API Errors
class PropertyNotFoundError(APIError):
    def __init__(self, property_id: str):
        super().__init__(
            f"Property {property_id} not found",
            status_code=404
        )

class ValidationFailedError(APIError):
    def __init__(self, message: str):
        super().__init__(
            message,
            status_code=400
        )

class UnauthorizedError(APIError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message,
            status_code=401
        )