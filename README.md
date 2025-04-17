# 微博超话自动签到

自动完成微博超话签到任务的容器应用。

## 功能特点

- 自动签到微博超话
- 支持多账号配置
- 支持自定义签到时间
- 支持 [Bark](https://github.com/Finb/Bark) 推送签到结果
- 基于容器运行，方便部署

## 使用方法

1. 复制 `.env.example` 为 `.env` 并修改配置：
   ```bash
   cp .env.example .env
   ```

2. 修改 `.env` 文件中的配置项：
   - `WEIBO_ACCOUNTS`: JSON 格式的账号配置数组，每个账号包含：
     - `name`: 账号名称（用于日志显示）
     - `card_list_cookie_url`: 微博超话签到 URL（使用微博轻享版进入超话列表自行抓包，类似 https://api.weibo.cn/2/cardlist?xxxxxxxxxxxx 这样的 url）
   - `BARK_KEY`: Bark 推送密钥（用于接收签到结果通知）
   - `CRON_SCHEDULE`: 定时任务时间（Cron 格式，默认每天早上 7 点）
   - `BARK_SERVER`: Bark 服务器地址（可选，默认为 https://api.day.app）

3. 构建容器镜像：
   ```bash
   podman build -t weibo-signin .
   ```

4. 运行容器：
   ```bash
   podman run -d --name weibo-signin weibo-signin
   ```

## 环境变量说明

- `WEIBO_ACCOUNTS`: JSON 格式的账号配置数组
- `BARK_KEY`: Bark 推送密钥
- `CRON_SCHEDULE`: Cron 定时配置（默认每天早上 7 点）
- `BARK_SERVER`: Bark 服务器地址（默认：https://api.day.app）
- `TZ`: 时区设置（默认：Asia/Shanghai）

## 多账号配置示例

```bash
# 注意：JSON 必须写在同一行
WEIBO_ACCOUNTS='[{"name":"账号1","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?xxx"},{"name":"账号2","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?yyy"}]'
```

## 注意事项

- 请确保 `.env` 文件中的配置格式正确，特别是 JSON 格式的账号配置必须写在同一行
- Bark 通知将使用统一的推送密钥，所有账号的签到结果都会发送到同一个设备
- 容器会根据 CRON_SCHEDULE 设置的时间定时执行所有账号的签到任务
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

- 查看定时任务日志：
  ```bash
  podman exec weibo-signin cat /var/log/cron.log
  ```