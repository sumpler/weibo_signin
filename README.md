# 微博超话自动签到

[English](./README.en.md) | [中文](./README.md)

自动完成微博超话签到任务的容器应用。支持 Docker 部署。

## 功能特点

- ✨ 自动签到微博超话
- 👥 支持多账号配置
- ⏰ 支持自定义签到时间
- 📱 支持 [Bark](https://github.com/Finb/Bark)、[Server酱](https://sct.ftqq.com/)、[企业微信](https://work.weixin.qq.com/) 推送签到结果
- 🐳 支持 Docker 容器化部署

## 快速开始

### 1. 配置文件准备

复制配置文件模板：
```bash
cp .env.example .env
```

### 2. 修改配置

编辑 `.env` 文件，配置以下必要参数：

| 参数 | 说明 | 示例 |
|------|------|------|
| `WEIBO_ACCOUNTS` | 账号配置（JSON 格式） | 见下方示例 |
| `BARK_KEY` | Bark 推送密钥（可选） | `xxxxxxxx` |
| `SERVERCHAN_KEY` | Server酱推送密钥（可选） | `xxxxxxxx` |
| `WECOM_CORPID` | 企业微信企业ID（可选） | `wwxxxxxxxxxxxxxxxx` |
| `WECOM_AGENTID` | 企业微信应用ID（可选） | `1000001` |
| `WECOM_SECRET` | 企业微信应用Secret（可选） | `xxxxxxxx` |
| `CRON_SCHEDULE` | 定时任务时间（Cron 格式） | `0 7 * * *`（每天7点） |

### 3. 运行容器

#### 使用 Docker

```bash
# 构建镜像
docker build -t weibo-signin .

# 运行容器
docker run -d --name weibo-signin -v $(pwd)/.env:/app/.env weibo-signin
```

#### 使用 Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

## 多账号配置示例

```bash
# 注意：JSON 必须写在同一行
WEIBO_ACCOUNTS='[{"name":"账号1","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?xxx"},{"name":"账号2","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?yyy"}]'
```

## 获取超话签到 URL

1. 使用微博轻享版 App 登录账号
2. 进入超话列表页面
3. 使用抓包工具（如 Charles、Fiddler、Stream）抓取请求
4. 找到类似 `https://api.weibo.cn/2/cardlist?xxxxxxxxxxxx` 的请求 URL配置在 card_list_cookie_url

## 常用命令参考

### Docker 命令

```bash
# 查看容器日志
docker logs weibo-signin

# 查看定时任务日志
docker exec weibo-signin cat /var/log/cron.log

# 手动执行签到脚本
docker exec -it weibo-signin python3 /app/main.py

# 测试通知渠道
docker exec -it weibo-signin python3 /app/tests/test_notifications.py

# 容器管理
docker stop weibo-signin    # 停止容器
docker start weibo-signin   # 启动容器
docker rm weibo-signin     # 删除容器
docker ps -a               # 查看所有容器状态
```

### 通知渠道测试

执行测试脚本后，将显示每个通知渠道的测试结果：

```bash
开始测试通知渠道...
--------------------------------------------------
渠道: Bark
状态: 成功
信息: 推送成功
--------------------------------------------------
渠道: Server酱
状态: 未配置
信息: SERVERCHAN_KEY 未设置
--------------------------------------------------
渠道: 企业微信
状态: 成功
信息: 推送成功
--------------------------------------------------
```

测试结果说明：
- 成功：通知渠道配置正确且可以正常推送
- 失败：通知渠道配置可能有误或服务异常
- 未配置：未设置该通知渠道的必要参数

## 注意事项

- 确保 `.env` 文件中的 WEIBO_ACCOUNTS 配置 JSON 格式正确且写在同一行
- 推送通知配置说明：
  - 需要配置 `BARK_KEY`、`SERVERCHAN_KEY` 或 `WECOM_SECRET` 中的至少一个
  - 如果配置多个，所有已配置的渠道都会收到推送通知
  - Bark 支持 iOS 设备推送
  - Server酱支持多个渠道推送签到结果
  - 企业微信配置需要同时设置 `WECOM_CORPID`、`WECOM_AGENTID` 和 `WECOM_SECRET`
- 容器将按照 `CRON_SCHEDULE` 设置的时间定时执行签到任务

## 问题反馈

如果在使用过程中遇到问题，欢迎提交 Issue 反馈。

## 许可证

本项目采用 [MIT 许可证](./LICENSE)。