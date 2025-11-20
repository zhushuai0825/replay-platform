FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 复制 requirements 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制全部代码
COPY . .

# Celery worker 启动命令
CMD ["celery", "-A", "app.celery_app.celery_app", "worker", "--loglevel=info"]


