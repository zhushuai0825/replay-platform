"""
Function : 读取和管理项目配置
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : settings.py
Describe : 通过 pydantic-settings 支持 .env 和环境变量
"""

from pathlib import Path  # 处理路径
from typing import List  # 引入 List，用于 CORS 白名单

from pydantic_settings import BaseSettings  # 基于 Pydantic 的配置基类


class Settings(BaseSettings):
    """统一存放应用所需的配置项"""

    APP_NAME: str = "replay-platform"  # 应用名称
    APP_ENV: str = "development"  # 当前环境（development/production/testing）
    APP_DEBUG: bool = True  # 是否开启调试模式
    APP_VERSION: str = "1.0.0"  # 版本号，便于接口展示

    API_V1_PREFIX: str = "/api/v1"  # 统一的 API 前缀

    # 默认使用 localhost，当 FastAPI 运行在 Docker 内时可改为 postgres
    DATABASE_URL: str = "postgresql://replay_user:replay_password@localhost:5432/replay_db"

    # Redis 相关配置（可以在 .env 中覆盖）
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # 静态资源 / 文件存储
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    DATA_DIR: Path = BASE_DIR / "data"
    TRAFFIC_FILE_STORAGE_PATH: str = str(DATA_DIR / "traffic")
    TRAFFIC_FILE_TEMP_PATH: str = str(DATA_DIR / "temp")
    TRAFFIC_FILE_MAX_SIZE: int = 50 * 1024 * 1024  # 50MB

    # CORS 白名单配置
    CORS_ALLOW_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True  # 是否允许携带 Cookie

    class Config:
        env_file = ".env"  # 指定 .env 文件路径
        case_sensitive = True  # 环境变量区分大小写


settings = Settings()  # 实例化配置，供项目其它模块导入使用

# 兼容 Celery CLI 直接读取模块级变量的写法
CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = settings.CELERY_RESULT_BACKEND
# 部分场景会尝试读取小写属性，提前提供
celery_broker_url = CELERY_BROKER_URL
celery_result_backend = CELERY_RESULT_BACKEND
