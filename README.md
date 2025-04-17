# 微博超话自动签到

自动完成微博超话签到任务的容器应用。

## 功能特点

- 自动签到微博超话
- 支持自定义签到时间
- 支持 [Bark](https://github.com/Finb/Bark) 推送签到结果
- 基于容器运行，方便部署

## 使用方法

1. 复制 `.env.example` 为 `.env` 并修改配置：
   ```bash
   cp .env.example .env
   ```

2. 修改 `.env` 文件中的配置项：
   - `CARD_LIST_COOKIE_URL`: 微博超话签到 URL(使用微博轻享版进入超话列表自行抓包，类似 https://api.weibo.cn/2/cardlist?xxxxxxxxxxxx 这样的 url)
   - `CRON_SCHEDULE`: 定时任务时间（Cron 格式）
   - `BARK_KEY`: Bark 推送密钥
   - `BARK_SERVER`: Bark 服务器地址

3. 构建容器镜像：
   ```bash
   podman build -t weibo-signin .
   ```

4. 运行容器：
   ```bash
   podman run -d --name weibo-signin weibo-signin
   ```

## 环境变量说明

- `CARD_LIST_COOKIE_URL`: 微博超话签到 URL
- `CRON_SCHEDULE`: Cron 定时配置（默认每天早上 7 点）
- `BARK_KEY`: Bark 推送密钥
- `BARK_SERVER`: Bark 服务器地址
- `TZ`: 时区设置（默认：Asia/Shanghai）

## 注意事项

- 请确保 `.env` 文件中的 URL 和密钥配置正确
- 容器会根据 CRON_SCHEDULE 设置的时间定时执行签到任务
- 可以通过查看容器日志了解签到状态：
  ```bash
  podman logs weibo-signin
  ```

## 其他常用命令

- 停止容器：
  ```bash
  podman stop weibo-signin
  ```

- 启动已停止的容器：
  ```bash
  podman start weibo-signin
  ```

- 删除容器：
  ```bash
  podman rm weibo-signin
  ```

- 查看容器状态：
  ```bash
  podman ps -a
  ``` 