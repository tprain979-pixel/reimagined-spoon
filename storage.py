"""
数据存储模块 - 管理已推送新闻记录
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Set


class NewsStorage:
    """管理已推送新闻的存储和去重"""

    def __init__(self, storage_file: str = "sent_news.json"):
        self.storage_file = storage_file
        self.sent_news = self._load_storage()

    def _load_storage(self) -> Dict:
        """加载已推送新闻记录"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载存储文件失败: {e}")
                return {"news": []}
        return {"news": []}

    def _save_storage(self):
        """保存新闻记录到文件"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.sent_news, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存存储文件失败: {e}")

    def is_news_sent(self, news_title: str, news_url: str = None) -> bool:
        """检查新闻是否已推送（基于标题和URL）"""
        for news in self.sent_news.get("news", []):
            # 标题匹配或URL匹配都认为是重复
            if news.get("title") == news_title:
                return True
            if news_url and news.get("url") == news_url:
                return True
        return False

    def add_sent_news(self, news_items: List[Dict]):
        """添加已推送的新闻"""
        if "news" not in self.sent_news:
            self.sent_news["news"] = []

        timestamp = datetime.now().isoformat()
        for item in news_items:
            self.sent_news["news"].append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "sent_at": timestamp
            })

        self._save_storage()

    def cleanup_old_news(self, days: int = 30):
        """清理超过指定天数的旧新闻记录"""
        cutoff_date = datetime.now() - timedelta(days=days)

        if "news" in self.sent_news:
            self.sent_news["news"] = [
                news for news in self.sent_news["news"]
                if datetime.fromisoformat(news.get("sent_at", "1970-01-01")) > cutoff_date
            ]
            self._save_storage()

    def get_new_news(self, all_news: List[Dict]) -> List[Dict]:
        """过滤出未推送的新闻"""
        new_news = []
        for news in all_news:
            if not self.is_news_sent(news.get("title", ""), news.get("url")):
                new_news.append(news)
        return new_news
