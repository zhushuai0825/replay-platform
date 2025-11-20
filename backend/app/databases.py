"""
Function : 数据库引擎和 Session 管理
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : databases.py
Describe : 为 FastAPI 提供统一的数据库会话获取方法
"""

from sqlalchemy import create_engine  # 创建数据库引擎
from sqlalchemy.orm import declarative_base, sessionmaker  # 声明式基类与会话工厂

from .config.settings import settings  # 导入配置，获取 DATABASE_URL

# 创建数据库引擎，pool_pre_ping=True 可自动检测断开的连接
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 创建 sessionmaker，统一关闭自动提交与自动刷新
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 所有 ORM 模型需要继承的 Base
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入使用的数据库会话生成器"""

    db = SessionLocal()  # 实例化一个独立的 Session
    try:
        yield db  # 将 Session 暴露给调用方
    finally:
        db.close()  # 无论成功或异常都确保释放连接
