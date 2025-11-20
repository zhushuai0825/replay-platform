"""
Function:
Project:全链路
Author:Zhu Shuai
File:settings.py
Date:2025/11/19 22:09
Describe:

"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "replay-platform"
    APP_ENV: str = "development"  # development/production/testing
    APP_DEBUG: bool = True
    APP_VERSION: str = "1.0.0"

    API_V1_PREFIX:str = "/api/v1"
    # 默认使用 localhost，可以通过环境变量覆盖（例如 Docker 环境使用 postgres）
    DATABASE_URL: str = "postgresql://replay_user:replay_password@localhost:5432/replay_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"]
    CORS_ALLOW_CREDENTIALS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()