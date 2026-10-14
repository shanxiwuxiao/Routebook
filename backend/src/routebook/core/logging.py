import logging
import sys
from typing import Any

import structlog
from structlog.stdlib import ProcessorFormatter

from routebook.core.config import settings

# 两个日志链路共用的「前处理」：
#   1. structlog 自己打的日志（logger.info(...)）
#   2. 第三方库（uvicorn / httpx / sqlalchemy）走 stdlib logging 打的日志
# 注意：这里**不能**放 renderer —— renderer 只属于最后那一步，放进来会重复渲染。
shared_processors: list[Any] = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
]


def configure_logging(level: str | None = None) -> None:
    """配置 stdlib logging + structlog。

    不传 level 时读 settings.LOG_LEVEL。幂等：重复调用不会叠加 handler。
    """
    log_level = getattr(logging, (level or settings.LOG_LEVEL).upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # 真终端用彩色控制台，容器里/管道里用 JSON，便于日志采集
    # ensure_ascii=False：否则中文会被转成 \uXXXX，docker logs 里没法看
    renderer: Any = (
        structlog.dev.ConsoleRenderer()
        if sys.stdout.isatty()
        else structlog.processors.JSONRenderer(ensure_ascii=False)
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(
        ProcessorFormatter(
            # 第三方库的 LogRecord 先在这里转成 structlog 的 event_dict
            foreign_pre_chain=shared_processors,
            processors=[
                # ⚠️ 这一行不能省：少了 remove_processors_meta，
                # 输出里会混进 _record / _from_structlog 两个巨大的原始字段
                ProcessorFormatter.remove_processors_meta,
                renderer,
            ],
        )
    )

    for existing in list(root_logger.handlers):
        root_logger.removeHandler(existing)
    root_logger.addHandler(handler)

    structlog.configure(
        # 自己打的日志：走完共用前处理后，交给 ProcessorFormatter 统一渲染
        processors=[*shared_processors, ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()
