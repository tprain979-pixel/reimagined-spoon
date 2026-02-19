"""
飞书推送模块 - 发送消息到飞书
"""
import requests
import json
from typing import Dict, Optional


class FeishuSender:
    """飞书消息推送器"""

    def __init__(self, config: Dict):
        """
        初始化飞书推送器

        Args:
            config: 飞书配置，包含 app_id, app_secret, webhook_url 等
        """
        self.app_id = config.get("app_id")
        self.app_secret = config.get("app_secret")
        self.webhook_url = config.get("webhook_url")
        self.chat_id = config.get("chat_id")
        self.tenant_access_token = None

    def get_tenant_access_token(self) -> Optional[str]:
        """
        获取飞书 tenant_access_token

        Returns:
            access_token 或 None
        """
        if not self.app_id or not self.app_secret:
            print("[飞书推送] 缺少 app_id 或 app_secret")
            return None

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()

            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                print("[飞书推送] 成功获取 access_token")
                return self.tenant_access_token
            else:
                print(f"[飞书推送] 获取 token 失败: {result}")
                return None
        except Exception as e:
            print(f"[飞书推送] 获取 token 异常: {e}")
            return None

    def send_via_webhook(self, content: str, title: str = "物流预警") -> bool:
        """
        通过 Webhook 发送消息

        Args:
            content: 消息内容（支持 Markdown）
            title: 消息标题

        Returns:
            是否发送成功
        """
        if not self.webhook_url:
            print("[飞书推送] 未配置 webhook_url")
            return False

        data = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content
                    }
                ]
            }
        }

        try:
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=10
            )
            result = response.json()

            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print(f"[飞书推送] Webhook 发送成功: {title}")
                return True
            else:
                print(f"[飞书推送] Webhook 发送失败: {result}")
                return False
        except Exception as e:
            print(f"[飞书推送] Webhook 发送异常: {e}")
            return False

    def send_via_bot(self, content: str, title: str = "物流预警") -> bool:
        """
        通过机器人发送消息到指定群聊

        Args:
            content: 消息内容（支持 Markdown）
            title: 消息标题

        Returns:
            是否发送成功
        """
        if not self.chat_id:
            print("[飞书推送] 未配置 chat_id")
            return False

        # 获取 access_token
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False

        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "receive_id": self.chat_id,
            "msg_type": "interactive",
            "content": json.dumps({
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": content
                    }
                ]
            })
        }

        params = {"receive_id_type": "chat_id"}

        try:
            response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
            result = response.json()

            if result.get("code") == 0:
                print(f"[飞书推送] 机器人发送成功: {title}")
                return True
            else:
                print(f"[飞书推送] 机器人发送失败: {result}")
                return False
        except Exception as e:
            print(f"[飞书推送] 机器人发送异常: {e}")
            return False

    def send_message(self, content: str, title: str = "物流预警") -> bool:
        """
        发送消息（自动选择 webhook 或机器人方式）

        Args:
            content: 消息内容
            title: 消息标题

        Returns:
            是否发送成功
        """
        # 优先使用 webhook（更简单）
        if self.webhook_url:
            return self.send_via_webhook(content, title)

        # 否则使用机器人
        if self.app_id and self.app_secret and self.chat_id:
            return self.send_via_bot(content, title)

        print("[飞书推送] 未配置任何推送方式（webhook 或 机器人）")
        return False
