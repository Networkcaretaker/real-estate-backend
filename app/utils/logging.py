import structlog
import logging
import sys
from typing import Any, Dict
import os
from datetime import datetime

def setup_logging():
    """Configure structured logging"""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=os.getenv("LOG_LEVEL", "INFO"),
    )

    # Add timestamps to structured logging
    def add_timestamp(logger: Any, method_name: str, event_dict: Dict) -> Dict:
        event_dict["timestamp"] = datetime.utcnow().isoformat()
        return event_dict

    # Add environment info
    def add_env_info(logger: Any, method_name: str, event_dict: Dict) -> Dict:
        event_dict["environment"] = os.getenv("APP_ENV", "development")
        return event_dict

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            add_timestamp,
            add_env_info,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

def get_logger(name: str):
    """Get a logger instance"""
    return structlog.get_logger(name)