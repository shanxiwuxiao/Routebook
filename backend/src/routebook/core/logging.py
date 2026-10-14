import logging
import sys
from typing import Any

import structlog
from structlog.stdlib import ProcessorFormatter
from routebook.core.config import settings

def configure_logging() -> None:

    root_logger = logging.getLogger()
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    root_logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if sys.stderr.isatty():
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    handler.setFormatter(ProcessorFormatter(processors=processors))
    root_logger.addHandler(handler)

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()