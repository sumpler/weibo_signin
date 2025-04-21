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
        # 企业微信配置
        self.wecom_corpid = os.getenv('WECOM_CORPID')
        self.wecom_secret = os.getenv('WECOM_SECRET')
        self.wecom_agentid = os.getenv('WECOM_AGENTID')
        
    def send(self, title, content):
        """
        发送通知到所有已配置的渠道
        
        Args:
            title (str): 通知标题
            content (str): 通知内容
        """
        if not any([self.bark_key, self.serverchan_key, self.wecom_secret]):
            logger.warning("未配置任何通知渠道")
            return
            
        if self.bark_key:
            self._send_bark(title, content)
            
        if self.serverchan_key:
            self._send_serverchan(title, content)
            
        if self.wecom_corpid and self.wecom_agentid and self.wecom_secret:
            self._send_wecom(title, content)
    
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
            
    def _send_wecom(self, title, content):
        """
        发送企业微信通知
        
        Args:
            title (str): 通知标题
            content (str): 通知内容
        """
        try:
            # 获取访问令牌
            token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wecom_corpid}&corpsecret={self.wecom_secret}"
            token_resp = requests.get(token_url)
            token_result = token_resp.json()
            
            if token_result.get("errcode") != 0:
                logger.error(f"企业微信获取 access_token 失败: {token_result.get('errmsg')}")
                return
                
            access_token = token_result.get("access_token")
                
            # 发送消息
            send_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            
            message = {
                "touser": "@all",
                "msgtype": "text",
                "agentid": int(self.wecom_agentid),
                "text": {
                    "content": f"{title}\n\n{content}"
                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 1,
                "duplicate_check_interval": 1800
            }
            
            response = requests.post(send_url, json=message)
            result = response.json()
            
            if result.get("errcode") != 0:
                logger.error(f"企业微信通知发送失败: {result.get('errmsg')}")
            else:
                logger.info("企业微信通知发送成功")
                
        except Exception as e:
            logger.error(f"企业微信通知发送异常: {str(e)}")
