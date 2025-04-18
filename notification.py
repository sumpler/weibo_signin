import os
import logging
import requests
from dotenv import load_dotenv
from serverchan_sdk import sc_send


# 配置日志
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()


class Notification:
    """通知发送器，支持多种通知渠道"""
    
    def __init__(self):
        """初始化通知渠道配置"""
        self.bark_key = os.getenv('BARK_KEY')
        self.serverchan_key = os.getenv('SERVERCHAN_KEY')
        
    def send(self, title, content):
        """
        发送通知到所有已配置的渠道
        
        Args:
            title (str): 通知标题
            content (str): 通知内容
        """
        if not any([self.bark_key, self.serverchan_key]):
            logger.warning("未配置任何通知渠道")
            return
            
        if self.bark_key:
            self._send_bark(title, content)
            
        if self.serverchan_key:
            self._send_serverchan(title, content)
    
    def _send_bark(self, title, content):
        """
        发送 Bark 通知
        
        Args:
            title (str): 通知标题
            content (str): 通知内容
        """
        url = f"https://api.day.app/{self.bark_key}/{title}/{content}"
        try:
            response = requests.get(url)
            if response.status_code != 200:
                logger.error(f"Bark 通知发送失败: {response.status_code}")
        except Exception as e:
            logger.error(f"Bark 通知发送异常: {str(e)}")
    
    def _send_serverchan(self, title, content):
        """
        发送 ServerChan 通知
        
        Args:
            title (str): 通知标题
            content (str): 通知内容
        """
        response = sc_send(self.serverchan_key, title, content)
        if response.get("code") != 0:
            logger.error(f"ServerChan 通知发送失败: {response.get('message')}")
