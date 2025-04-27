# Weibo Super Topic Auto Sign-in

[English](./README.en.md) | [中文](./README.md)

A containerized application for automatically completing Weibo Super Topic sign-in tasks. Supports Docker deployment.

## Features

- ✨ Automatic Weibo Super Topic sign-in
- 👥 Multiple account support
- ⏰ Customizable sign-in schedule
- 📱 Supports [Bark](https://github.com/Finb/Bark), [ServerChan](https://sct.ftqq.com/), and [WeCom](https://work.weixin.qq.com/) push notifications
- 🐳 Docker container deployment support

## Quick Start

### 1. Prepare Configuration File

Copy the configuration template:
```bash
cp .env.example .env
```

### 2. Modify Configuration

Edit the `.env` file and configure the following required parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `WEIBO_ACCOUNTS` | Account configuration (JSON format) | See example below |
| `BARK_KEY` | Bark push key (optional) | `xxxxxxxx` |
| `SERVERCHAN_KEY` | ServerChan push key (optional) | `xxxxxxxx` |
| `WECOM_CORPID` | WeCom Corporation ID (optional) | `wwxxxxxxxxxxxxxxxx` |
| `WECOM_AGENTID` | WeCom Application ID (optional) | `1000001` |
| `WECOM_SECRET` | WeCom Application Secret (optional) | `xxxxxxxx` |
| `CRON_SCHEDULE` | Scheduled task time (Cron format) | `0 7 * * *` (7:00 AM daily) |

### 3. Run Container

#### Using Docker

```bash
# Build image
docker build -t weibo-signin .

# Run container
docker run -d --name weibo-signin -v $(pwd)/.env:/app/.env weibo-signin
```

#### Using Docker Compose (Recommended)

```bash
# Build and start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down

# Restart service
docker-compose restart
```

## Multiple Account Configuration Example

```bash
# Note: JSON must be written in a single line
WEIBO_ACCOUNTS='[{"name":"Account1","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?xxx"},{"name":"Account2","card_list_cookie_url":"https://api.weibo.cn/2/cardlist?yyy"}]'
```

## How to Get Super Topic Sign-in URL

1. Log in to your Weibo account using the Weibo Lite App
2. Navigate to the Super Topic list page
3. Use a packet capture tool (such as Charles, Fiddler, or Stream) to capture requests
4. Find a request URL similar to `https://api.weibo.cn/2/cardlist?xxxxxxxxxxxx` and configure it as card_list_cookie_url

## Common Commands Reference

### Docker Commands

```bash
# View container logs
docker logs weibo-signin

# View scheduled task logs
docker exec weibo-signin cat /var/log/cron.log

# Manually run the sign-in script
docker exec -it weibo-signin python3 /app/main.py

# Test notification channels
docker exec -it weibo-signin python3 /app/tests/test_notifications.py

# Container management
docker stop weibo-signin    # Stop container
docker start weibo-signin   # Start container
docker rm weibo-signin     # Remove container
docker ps -a               # View all container statuses
```

### Notification Channel Testing

After running the test script, it will display the test results for each notification channel:

```bash
Starting notification channel tests...
--------------------------------------------------
Channel: Bark
Status: Success
Message: Push successful
--------------------------------------------------
Channel: ServerChan
Status: Not Configured
Message: SERVERCHAN_KEY not set
--------------------------------------------------
Channel: WeCom
Status: Success
Message: Push successful
--------------------------------------------------
```

Test Result Explanation:
- Success: The notification channel is correctly configured and can push notifications
- Failed: The notification channel configuration might be incorrect or the service is experiencing issues
- Not Configured: Required parameters for this notification channel are not set

## Important Notes

- Ensure the JSON format in the `.env` file's WEIBO_ACCOUNTS configuration is correct and written in a single line
- Push notification configuration:
  - At least one of `BARK_KEY`, `SERVERCHAN_KEY`, or `WECOM_SECRET` must be configured
  - If multiple channels are configured, notifications will be sent to all configured channels
  - Bark supports iOS device push notifications
  - ServerChan supports multiple channel push notifications
  - WeCom configuration requires all three parameters: `WECOM_CORPID`, `WECOM_AGENTID`, and `WECOM_SECRET`
- The container will execute sign-in tasks according to the time set in `CRON_SCHEDULE`

## Issue Reporting

If you encounter any issues during use, please feel free to submit an Issue.

## License

This project is licensed under the [MIT License](./LICENSE). 