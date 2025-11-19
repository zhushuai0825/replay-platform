"""
Function:
Project:全链路
Author:Zhu Shuai
File:main.py
Date:2025/11/19 22:13
Describe:

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from databases import Base, engine


if settings.APP_DEBUG:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Replay Platform API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION}

@app.get("/health")
async def health():
    return {"status": "healthy"}

from app.api.v1 import tasks, traffic, environments
app.include_router(tasks.router, prefix=f"{settings.API_V1_PREFIX}/tasks", tags=["tasks"])
app.include_router(traffic.router, prefix=f"{settings.API_V1_PREFIX}/traffic", tags=["traffic"])
app.include_router(environments.router, prefix=f"{settings.API_V1_PREFIX}/environments", tags=["environments"])