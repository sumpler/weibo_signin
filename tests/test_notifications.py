import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载 .env 文件
load_dotenv()

class NotificationTester:
    def __init__(self):
        self.test_message = f"通知渠道测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.results = []

    def test_bark(self):
        """测试 Bark 通知"""
        bark_key = os.getenv('BARK_KEY')
        if not bark_key:
            self.results.append(("Bark", "未配置", "BARK_KEY 未设置"))
            return

        try:
            url = f"https://api.day.app/{bark_key}/{self.test_message}"
            response = requests.get(url)
            if response.status_code == 200:
                self.results.append(("Bark", "成功", "推送成功"))
            else:
                self.results.append(("Bark", "失败", f"HTTP状态码: {response.status_code}"))
        except Exception as e:
            self.results.append(("Bark", "失败", str(e)))

    def test_serverchan(self):
        """测试 Server酱通知"""
        serverchan_key = os.getenv('SERVERCHAN_KEY')
        if not serverchan_key:
            self.results.append(("Server酱", "未配置", "SERVERCHAN_KEY 未设置"))
            return

        try:
            url = f"https://sctapi.ftqq.com/{serverchan_key}.send"
            data = {
                "title": "通知测试",
                "desp": self.test_message
            }
            response = requests.post(url, data=data)
            if response.status_code == 200:
                self.results.append(("Server酱", "成功", "推送成功"))
            else:
                self.results.append(("Server酱", "失败", f"HTTP状态码: {response.status_code}"))
        except Exception as e:
            self.results.append(("Server酱", "失败", str(e)))

    def test_wecom(self):
        """测试企业微信通知"""
        corpid = os.getenv('WECOM_CORPID')
        agentid = os.getenv('WECOM_AGENTID')
        secret = os.getenv('WECOM_SECRET')

        if not all([corpid, agentid, secret]):
            self.results.append(("企业微信", "未配置", "企业微信配置不完整"))
            return

        try:
            # 获取访问令牌
            token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}"
            token_response = requests.get(token_url)
            access_token = token_response.json().get('access_token')

            if not access_token:
                self.results.append(("企业微信", "失败", "获取访问令牌失败"))
                return

            # 发送消息
            send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            data = {
                "touser": "@all",
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": self.test_message
                }
            }
            response = requests.post(send_url, json=data)
            
            if response.status_code == 200 and response.json().get('errcode') == 0:
                self.results.append(("企业微信", "成功", "推送成功"))
            else:
                self.results.append(("企业微信", "失败", f"错误信息: {response.json()}"))
        except Exception as e:
            self.results.append(("企业微信", "失败", str(e)))

    def run_all_tests(self):
        """运行所有测试"""
        print("开始测试通知渠道...")
        print("-" * 50)

        self.test_bark()
        self.test_serverchan()
        self.test_wecom()

        print("\n测试结果:")
        print("-" * 50)
        for channel, status, message in self.results:
            status_color = '\033[92m' if status == "成功" else '\033[91m' if status == "失败" else '\033[93m'
            print(f"渠道: {channel}")
            print(f"状态: {status_color}{status}\033[0m")
            print(f"信息: {message}")
            print("-" * 50)

if __name__ == "__main__":
    tester = NotificationTester()
    tester.run_all_tests() 