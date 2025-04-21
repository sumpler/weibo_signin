# 使用 Python 3.9 作为基础镜像
FROM python:3.9-slim

# 设置环境变量
ENV TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /app

# 安装必要的工具
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    # 设置时区
    && ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone

# 复制 .env 文件
COPY .env .
RUN set -a && . ./.env && set +a

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建日志文件
RUN touch /var/log/cron.log

# 创建 cron 环境设置脚本
RUN echo '#!/bin/sh\n\
set -a\n\
. /app/.env\n\
set +a\n\
/usr/local/bin/python /app/main.py >> /var/log/cron.log 2>&1' > /app/cron_task.sh
RUN chmod +x /app/cron_task.sh

# 创建启动脚本
RUN echo '#!/bin/sh\n\
set -a\n\
. /app/.env\n\
set +a\n\
# 显示当前时区和时间\n\
echo "Container timezone: $(date)"\n\
echo "Timezone setting: $(cat /etc/timezone)"\n\
echo "$CRON_SCHEDULE /app/cron_task.sh" | crontab -\n\
service cron start\n\
echo "Cron service started..."\n\
echo "Current cron jobs:"\n\
crontab -l\n\
echo "Watching log file..."\n\
tail -f /var/log/cron.log' > /app/start.sh

RUN chmod +x /app/start.sh

# 运行 cron 和日志监控
CMD ["/app/start.sh"]