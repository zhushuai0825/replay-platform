"""
Function:
Project:全链路
Author:Zhu Shuai
File:databases.py
Date:2025/11/19 22:09
Describe:

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config.settings import settings

# pool_pre_ping=True解决数据库长时间不使用后连接被关闭的问题
engine = create_engine(settings.DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# get_db()生成数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()