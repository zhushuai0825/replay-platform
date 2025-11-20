"""
Celery 任务：模拟回放流程
"""

import time
from datetime import datetime

from ..celery_app import celery_app
from ..databases import SessionLocal
from ..models import ReplayTask
from ..utils.logger import logger


@celery_app.task(name="app.services.replay_engine.run_replay_task")
def run_replay_task(task_id: int) -> str:
    """模拟执行回放任务"""

    db = SessionLocal()
    task: ReplayTask | None = None
    try:
        task = db.query(ReplayTask).filter(ReplayTask.id == task_id).one_or_none()
        if not task:
            logger.warning("任务不存在: %s", task_id)
            return "task_not_found"

        task.status = "running"
        task.started_at = datetime.utcnow()
        task.total_requests = 5
        db.commit()

        for index in range(1, 6):
            time.sleep(1)
            task.completed_requests = index
            task.progress = int(index * 100 / task.total_requests)
            db.commit()

        task.status = "completed"
        task.completed_at = datetime.utcnow()
        db.commit()
        return "completed"
    except Exception:
        if task:
            task.status = "failed"
            db.commit()
        logger.exception("回放任务执行失败")
        raise
    finally:
        db.close()

