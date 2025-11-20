"""
流量文件相关 Schema
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel


class TrafficFileOut(BaseModel):
    id: int
    original_filename: str
    file_size: int
    file_type: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True


class TrafficFileListResponse(BaseModel):
    items: List[TrafficFileOut]
    total: int
    page: int
    page_size: int

