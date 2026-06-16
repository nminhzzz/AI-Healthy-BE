"""
core/config.py — Cấu hình toàn dự án qua environment variables.
Dùng pydantic-settings để tự động load từ file .env.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, MySQLDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Tất cả biến môi trường của HealthShop AI.
    Các giá trị được đọc từ file .env (hoặc biến môi trường hệ thống).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────────────────────────
    app_name: str = Field(default="HealthShop AI", description="Tên ứng dụng")
    app_env: Literal["development", "production", "testing"] = Field(
        default="development"
    )
    debug: bool = Field(default=False)
    secret_key: str = Field(..., description="Secret key bảo mật ứng dụng")

    # ── JWT ───────────────────────────────────────────────────────────────────
    jwt_secret_key: str = Field(..., description="Secret key ký JWT")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # ── MySQL ─────────────────────────────────────────────────────────────────
    mysql_host: str = Field(default="localhost")
    mysql_port: int = Field(default=3306)
    mysql_user: str = Field(default="root")
    mysql_password: str = Field(default="")
    mysql_db: str = Field(default="healthshop_ai")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """DSN kết nối MySQL cho SQLAlchemy (sync)."""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
            "?charset=utf8mb4"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        """DSN kết nối MySQL cho SQLAlchemy (async)."""
        return (
            f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
            "?charset=utf8mb4"
        )

    # ── MongoDB ───────────────────────────────────────────────────────────────
    mongodb_url: str = Field(default="mongodb://localhost:27017")
    mongodb_db: str = Field(default="healthshop_ai")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")
    redis_db: int = Field(default=0)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def redis_url(self) -> str:
        """URL kết nối Redis."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # ── OpenAI ────────────────────────────────────────────────────────────────
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4o")
    openai_embedding_model: str = Field(default="text-embedding-3-small")

    # ── CORS ──────────────────────────────────────────────────────────────────
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    # ── File Upload ───────────────────────────────────────────────────────────
    upload_dir: str = Field(default="uploads")
    max_file_size_mb: int = Field(default=10)

    # ── Cloudinary ────────────────────────────────────────────────────────────
    cloudinary_cloud_name: str = Field(default="")
    cloudinary_api_key: str = Field(default="")
    cloudinary_api_secret: str = Field(default="")

@lru_cache
def get_settings() -> Settings:
    """
    Singleton Settings — chỉ khởi tạo 1 lần nhờ lru_cache.
    Dùng trong FastAPI Dependency Injection:

        from app.core.config import get_settings
        settings = get_settings()
    """
    return Settings()


# Shortcut dùng trực tiếp trong code nội bộ
settings: Settings = get_settings()
