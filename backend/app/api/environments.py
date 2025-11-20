"""
Function : 环境管理接口
Project  : 全链路回放平台
Author   : Zhu Shuai
File     : environments.py
Describe : 提供环境列表示例
"""

from fastapi import APIRouter  # FastAPI 路由

router = APIRouter(prefix="", tags=["environments"])  # 创建路由


@router.get("/", summary="环境列表")
async def list_environments():
    """临时示例：返回空列表"""

    return {"environments": []}  # 可替换为真实查询逻辑
