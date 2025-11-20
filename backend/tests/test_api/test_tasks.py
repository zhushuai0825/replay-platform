"""
示例测试：由于任务接口依赖真实数据库，此处仅验证接口可用
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_tasks_status_code():
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200