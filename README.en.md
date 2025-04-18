# Weibo Super Topic Auto Sign-in

[English](./README.en.md) | [中文](./README.md)

A containerized application for automatically completing Weibo Super Topic sign-in tasks. Supports Docker deployment.

## Features

- ✨ Automatic Weibo Super Topic sign-in
- 👥 Multiple account support
- ⏰ Customizable sign-in schedule
- 📱 Supports [Bark](https://github.com/Finb/Bark) and [ServerChan](https://sct.ftqq.com/) push notifications
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
| `BARK_KEY` | Bark push key (optional, at least one of BARK_KEY or SERVERCHAN_KEY required) | `xxxxxxxx` |
| `SERVERCHAN_KEY` | ServerChan push key (optional, at least one of BARK_KEY or SERVERCHAN_KEY required) | `xxxxxxxx` |
| `CRON_SCHEDULE` | Scheduled task time (Cron format) | `0 7 * * *` (7:00 AM daily) |
| `TZ` | Timezone setting (optional) | `Asia/Shanghai` |

### 3. Run Container

#### Using Docker

```bash
# Build image
docker build -t weibo-signin .

# Run container
docker run -d --name weibo-signin weibo-signin
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

# Container management
docker stop weibo-signin    # Stop container
docker start weibo-signin   # Start container
docker rm weibo-signin     # Remove container
docker ps -a               # View all container statuses
```

## Important Notes

- Ensure the JSON format in the `.env` file's WEIBO_ACCOUNTS configuration is correct and written in a single line
- Push notification configuration:
  - At least one of `BARK_KEY` or `SERVERCHAN_KEY` must be configured
  - If both are configured, notifications will be sent to both channels
  - Bark supports iOS device push notifications
  - ServerChan supports multiple channel push notifications
- The container will execute sign-in tasks according to the time set in `CRON_SCHEDULE`

## Issue Reporting

If you encounter any issues during use, please feel free to submit an Issue.

## License

This project is licensed under the [MIT License](./LICENSE). 