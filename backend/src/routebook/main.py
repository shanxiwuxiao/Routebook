import importlib.metadata
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging import configure_logging

configure_logging()

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # 参数名以下划线开头：M0 还用不到 app.state，ruff 的 ARG001 只忽略这类命名

    logger.info("Starting up the application...")
    yield
    logger.info("Shutting down the application...")


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        title="Routebook API",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    async def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "env": settings.ENV,
            "version": importlib.metadata.version("routebook"),
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("routebook.main:app", host="127.0.0.1", port=8000)
