# API 文档（当前版本）

## 基础信息

- 后端地址：`http://localhost:8000`
- 前缀：`/api/v1`
- 所有接口返回 JSON，示例：`{"items": [], "total": 0}`

---

## 1. 任务

### GET `/api/v1/tasks/`

| 参数        | 说明           | 默认 |
|-------------|----------------|------|
| `page`      | 页码 (>=1)     | 1    |
| `page_size` | 每页条数 (<=100) | 10   |

**响应示例**
```json
{
  "items": [
    {
      "id": 1,
      "name": "demo",
      "status": "pending",
      "progress": 0,
      "total_requests": 0,
      "completed_requests": 0,
      "failed_requests": 0,
      "created_at": "2025-11-20T11:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### POST `/api/v1/tasks/`

**Body**
```json
{
  "name": "demo task",
  "traffic_file_id": 1,
  "environment_id": 1
}
```

创建成功会触发 Celery 任务 `app.services.replay_engine.run_replay_task`。

---

## 2. 流量文件

### GET `/api/v1/traffic/`

参数同任务列表，增加 `search`（按原始文件名模糊搜索）。

### POST `/api/v1/traffic/upload`

- `multipart/form-data`
- 字段：`file`（HAR/JSON），最大 50MB

---

## 3. 环境

目前仅有占位接口 `GET /api/v1/environments/`，返回空列表，后续再补充。

---

## 4. 系统/监控

- `/`：返回应用名称和版本
- `/health`：健康检查
- `/metrics`：Prometheus 指标（需启动后端才可访问）

---

## Postman/Thunder Client

建议创建环境变量：

| 名称     | 值                    |
|----------|------------------------|
| base_url | `http://localhost:8000` |

示例请求：`{{base_url}}/api/v1/tasks/?page=1&page_size=10`

---

## 待补充

- 任务详情、结果列表
- 环境/流量管理的完整 CRUD
- 鉴权相关接口

