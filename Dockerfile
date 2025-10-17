# 使用Python 3.9官方镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py

# 保持系统默认 apt 源，避免某些基础镜像缺失 sources.list 导致报错

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY backend/requirements.txt .

# 安装Python依赖（使用官方PyPI，Zeabur国际环境更稳定）
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制backend目录下的应用代码
COPY backend/ .

# 创建非root用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口（Zeabur 会通过 $PORT 环境变量指定）
EXPOSE 5002

# 启动命令（支持 Zeabur 的 $PORT 环境变量，默认 5002）
CMD gunicorn --bind 0.0.0.0:${PORT:-5002} --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile - run:app

