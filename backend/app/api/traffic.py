"""
Function:
Project:全链路
Author:Zhu Shuai
File:traffic.py
Date:2025/11/19 22:10
Describe:

"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_traffic():
    return {"traffic": []}
