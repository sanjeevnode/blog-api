from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # This config let the settings object to load variables from the .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # ── App settings ──────────────────────────────────────────────────────
    PROJECT_NAME: str = "Blog"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    DEBUG : bool =True
    TIMEZONE: str = "Asia/Kolkata"

    # ── Security / JWT ────────────────────────────────────────────────────
    SECRET_KEY: str = "super_secre_key_ttynjbhfs939nicns929nfnkkalldf883j"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    # ── Database ──────────────────────────────────────────────────────────
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 7211
    POSTGRES_USER: str = "blog"
    POSTGRES_PASSWORD: str = "blog"
    POSTGRES_DB: str = "blog"

    # We use @computed_field so that this database URL is constructed 
    # dynamically and can be validated by Pydantic.

    @computed_field # type: ignore[decorator]
    @property
    def get_database_url(self) -> str:
        return(
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ── Redis ─────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:7213/0"
    OTP_EXPIRE_SECONDS: int = 300          # 5 min

    # ── S3 / RustFS ───────────────────────────────────────────────────────
    S3_ENDPOINT_URL: str = "http://localhost:7214"
    S3_ACCESS_KEY: str = "rustfsadmin"
    S3_SECRET_KEY: str = "rustfsadmin"
    S3_BUCKET_NAME: str = "blog-media"
    S3_PUBLIC_BASE_URL: str = "http://localhost:7214/blog-media"

    # ── Email / Mailpit ───────────────────────────────────────────────────
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 7216
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@blog.local"
    EMAIL_FROM_NAME: str = "Blog"

    # ── CORS ──────────────────────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

# caching settings avoids reading the filesystem multiple times for configuration
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
