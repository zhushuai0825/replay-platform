"""
流量文件上传与列表
"""

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from ..config.settings import settings
from ..databases import get_db
from ..models import TrafficFile
from ..schemas.traffic import TrafficFileListResponse, TrafficFileOut
from ..utils.logger import logger

router = APIRouter(prefix="", tags=["traffic"])

STORAGE_PATH = Path(settings.TRAFFIC_FILE_STORAGE_PATH)
TEMP_PATH = Path(settings.TRAFFIC_FILE_TEMP_PATH)
for path in (STORAGE_PATH, TEMP_PATH):
    Path(path).mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=TrafficFileListResponse, summary="流量文件列表")
async def list_traffic(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: str | None = Query(None, description="按原始文件名模糊搜索"),
    db: Session = Depends(get_db),
):
    query = db.query(TrafficFile)
    if search:
        query = query.filter(TrafficFile.original_filename.ilike(f"%{search}%"))
    total = query.count()
    items = (
        query.order_by(TrafficFile.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/upload", response_model=TrafficFileOut, summary="上传流量文件")
async def upload_traffic_file(
    file: UploadFile = File(..., description="HAR/JSON 文件"),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    unique_name = f"{uuid4().hex}_{file.filename}"
    save_path = STORAGE_PATH / unique_name
    total_size = 0

    try:
        with save_path.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                total_size += len(chunk)
                if total_size > settings.TRAFFIC_FILE_MAX_SIZE:
                    raise HTTPException(
                        status_code=400, detail="文件过大，超过限制"
                    )
                buffer.write(chunk)
    except HTTPException:
        save_path.unlink(missing_ok=True)
        raise
    except Exception as exc:  # noqa: BLE001
        save_path.unlink(missing_ok=True)
        logger.exception("写入流量文件失败")
        raise HTTPException(status_code=500, detail="保存文件失败") from exc

    record = TrafficFile(
        filename=unique_name,
        original_filename=file.filename,
        file_path=str(save_path),
        file_size=total_size,
        file_type=Path(file.filename).suffix.lstrip("."),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
