from  pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", env_file_encoding="utf-8", extra="ignore")

    ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str ="dev-secret"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = ""

    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    REDIS_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_BROKER_URL: str
    CELERY_TASK_ALWAYS_EAGER: bool = False

    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2048
    LLM_TIMEOUT_SECONDS: int = 60
    AI_NEXT_STEP_TIMEOUT_SECONDS: int = 5
    AI_NEXT_STEP_ENABLED: bool = True

    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIM: int = 1536

    RATE_LIMIT_ENABLED: bool = True

    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()


