"""
Function : 定义任务相关的 Pydantic Schema
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : task.py
Describe : FastAPI 接口的请求/响应模型
"""

from datetime import datetime  # 处理时间字段
from typing import List  # 列表类型

from pydantic import BaseModel  # Pydantic 基类


class TaskCreate(BaseModel):
    """创建任务时需要的字段"""

    name: str  # 任务名称
    traffic_file_id: int  # 关联的流量文件 ID
    environment_id: int  # 运行的环境 ID


class TaskOut(BaseModel):
    """返回给前端的任务信息"""

    id: int  # 任务 ID
    name: str  # 任务名称
    status: str  # 当前状态
    progress: int  # 进度
    total_requests: int  # 总请求数
    completed_requests: int  # 成功数
    failed_requests: int  # 失败数
    created_at: datetime  # 创建时间

    class Config:
        orm_mode = True  # 允许直接从 ORM 模型转换


class TaskListResponse(BaseModel):
    """任务列表响应"""

    items: List[TaskOut]  # 任务列表
    total: int  # 总条数
    page: int  # 当前页码
    page_size: int  # 每页大小
