"""
日志配置：使用 loguru 输出到 stdout 和本地文件
"""

from pathlib import Path
import sys

from loguru import logger

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 清除默认 handler，重新配置
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=False,
)
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="1 day",
    retention="7 days",
    encoding="utf-8",
    enqueue=True,
    serialize=True,
)

__all__ = ["logger"]
"""
日志配置
"""
import sys
from loguru import logger
from app.config import settings


def setup_logger():
    """配置日志记录器"""
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
    )
    
    # 添加文件输出
    if settings.LOG_FILE_PATH:
        logger.add(
            f"{settings.LOG_FILE_PATH}/app.log",
            rotation="100 MB",
            retention="10 days",
            level=settings.LOG_LEVEL,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )
    
    return logger


