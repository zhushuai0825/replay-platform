"""
Function : FastAPI 入口
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : main.py
Describe : 启动应用、配置 CORS、挂载路由
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from .config.settings import settings
from .databases import Base, engine
from .utils.logger import logger

# 调试模式下尝试自动建表
if settings.APP_DEBUG:
    try:
        Base.metadata.create_all(bind=engine)  # 根据模型创建表
        logger.info("Database tables created successfully")  # 成功日志
    except Exception as exc:  # 捕获异常但不中断服务
        logger.warning(
            "Failed to create database tables: %s. The application will continue to run.",
            exc,
        )

# 创建 FastAPI 实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Replay Platform API",
)

# 暴露 Prometheus 指标
Instrumentator().instrument(app).expose(app)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,  # 允许访问的域名
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,  # 是否允许携带 Cookie
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的请求头
)


@app.get("/", summary="欢迎页", tags=["system"])
async def root():
    """返回应用的基本信息"""

    return {"name": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health", summary="健康检查", tags=["system"])
async def health():
    """供监控系统调用的健康检查接口"""

    return {"status": "healthy"}


from .api import environments, tasks, traffic  # noqa: E402  # 导入路由模块

# 注册任务相关路由
app.include_router(
    tasks.router,
    prefix=f"{settings.API_V1_PREFIX}/tasks",
    tags=["tasks"],
)
# 注册流量文件相关路由
app.include_router(
    traffic.router,
    prefix=f"{settings.API_V1_PREFIX}/traffic",
    tags=["traffic"],
)
# 注册环境相关路由
app.include_router(
    environments.router,
    prefix=f"{settings.API_V1_PREFIX}/environments",
    tags=["environments"],
)
