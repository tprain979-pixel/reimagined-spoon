FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY *.py .
COPY config.json .
COPY sent_news.json .

# 创建日志目录
RUN mkdir -p /app/logs

# 设置时区（可选，根据需要修改）
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置环境变量（可通过 docker run -e 覆盖）
ENV TAVILY_API_KEY=""
ENV PYTHONUNBUFFERED=1

# 默认执行完整检查
CMD ["python", "logistics_alert.py", "both"]
