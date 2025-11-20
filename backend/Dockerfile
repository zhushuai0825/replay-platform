# 使用国内镜像源（如果 Docker Hub 无法访问）
# 可以尝试使用以下镜像源之一：
# FROM registry.cn-hangzhou.aliyuncs.com/google_containers/python:3.11-slim
# 或者使用官方镜像（如果网络正常）
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 先复制 requirements.txt 并安装依赖（利用 Docker 缓存层）
COPY requirements.txt .

# 配置 pip 使用国内镜像源（加速下载）
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
