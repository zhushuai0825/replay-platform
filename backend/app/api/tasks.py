"""
Function : 任务相关接口
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : tasks.py
Describe : 提供任务的查询与创建
"""

from fastapi import APIRouter, Depends, Query  # FastAPI 工具
from sqlalchemy.orm import Session  # SQLAlchemy Session 类型

from ..celery_app import celery_app
from ..databases import get_db  # 获取数据库会话
from ..models import ReplayTask  # 导入任务模型
from ..schemas.task import TaskCreate, TaskListResponse, TaskOut  # 导入 Schema
from ..utils.logger import logger

router = APIRouter(prefix="", tags=["tasks"])  # 创建路由实例


@router.get("/", response_model=TaskListResponse, summary="任务列表")
async def list_tasks(
    page: int = Query(1, ge=1, description="页码"),  # 分页页码
    page_size: int = Query(10, ge=1, le=100, description="每页条数"),  # 分页大小
    db: Session = Depends(get_db),  # 注入数据库 Session
):
    """分页查询任务"""

    query = db.query(ReplayTask)  # 构建查询
    total = query.count()  # 统计总数
    items = (
        query.order_by(ReplayTask.created_at.desc())  # 按创建时间倒序
        .offset((page - 1) * page_size)  # 跳过前面数据
        .limit(page_size)  # 限制条数
        .all()
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}  # 返回结果


@router.post("/", response_model=TaskOut, summary="创建任务")
async def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """创建新的回放任务"""

    task = ReplayTask(
        name=payload.name,
        traffic_file_id=payload.traffic_file_id,
        environment_id=payload.environment_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    try:
        celery_app.send_task(
            "app.services.replay_engine.run_replay_task",
            args=[task.id],
        )
    except Exception:  # noqa: BLE001
        logger.exception("发送 Celery 任务失败")

    return task
