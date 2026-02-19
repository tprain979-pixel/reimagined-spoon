#!/usr/bin/env python3
"""
GitHub Actions 版本 - 从环境变量读取配置
"""
import json
import sys
import os
import requests
from datetime import datetime
from typing import Dict, List

from weather_monitor import format_weather_report
from news_monitor import format_news_report, extract_news_items
from feishu_sender import FeishuSender
from storage import NewsStorage


def load_config_from_env() -> Dict:
    """从环境变量加载配置"""
    config = {
        "tavily_api_key": os.environ.get("TAVILY_API_KEY", ""),
        "feishu": {
            "webhook_url": os.environ.get("FEISHU_WEBHOOK_URL", "")
        },
        "monitoring": {
            "countries": ["Germany", "France", "Netherlands", "Belgium", "Poland"],
            "weather_keywords": ["extreme weather", "storm", "snow", "heavy rain", "transport disruption"],
            "news_keywords": ["strike", "fire", "warehouse", "port closure", "transport disruption", "logistics incident"]
        },
        "storage": {
            "sent_news_file": "sent_news.json",
            "max_history_days": 30
        }
    }

    # 验证必需配置
    if not config["tavily_api_key"]:
        print("❌ 错误：未设置 TAVILY_API_KEY 环境变量")
        sys.exit(1)

    if not config["feishu"]["webhook_url"]:
        print("❌ 错误：未设置 FEISHU_WEBHOOK_URL 环境变量")
        sys.exit(1)

    return config


def search_with_tavily(api_key: str, query: str, max_results: int = 10) -> List[Dict]:
    """使用 Tavily API 搜索"""
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "days": 1
    }

    try:
        print(f"[Tavily] 搜索: {query[:60]}...")
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])
            print(f"[Tavily] ✅ 找到 {len(results)} 条结果")
            return results
        else:
            print(f"[Tavily] ❌ 失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"[Tavily] ❌ 异常: {e}")
        return []


def check_weather(config: Dict, feishu: FeishuSender):
    """检查天气预警"""
    print("\n" + "="*60)
    print(f"[天气预警] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    countries = " OR ".join(config["monitoring"]["countries"])
    keywords = " ".join(config["monitoring"]["weather_keywords"])
    query = f"({countries}) logistics transport weather {keywords}"

    results = search_with_tavily(config["tavily_api_key"], query, 10)
    report = format_weather_report(results)

    print("\n[天气预警] 推送到飞书...")
    if feishu.send_message(report, title="欧洲物流天气预警"):
        print("[天气预警] ✅ 成功")
    else:
        print("[天气预警] ❌ 失败")


def check_news(config: Dict, feishu: FeishuSender, storage: NewsStorage):
    """检查物流新闻"""
    print("\n" + "="*60)
    print(f"[物流新闻] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    countries = " OR ".join(config["monitoring"]["countries"])
    keywords = " OR ".join(config["monitoring"]["news_keywords"])
    query = f"({countries}) logistics ({keywords})"

    results = search_with_tavily(config["tavily_api_key"], query, 15)
    all_news = extract_news_items(results)
    new_news = storage.get_new_news(all_news)

    print(f"[物流新闻] 总共: {len(all_news)}, 新增: {len(new_news)}")

    if new_news:
        report = format_news_report(new_news)
        if report:
            print("\n[物流新闻] 推送到飞书...")
            if feishu.send_message(report, title="欧洲物流突发事件预警"):
                storage.add_sent_news(new_news)
                print("[物流新闻] ✅ 成功")
            else:
                print("[物流新闻] ❌ 失败")
    else:
        print("[物流新闻] ℹ️ 无新增，跳过推送")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python logistics_alert_github.py [weather|news|both]")
        sys.exit(1)

    check_type = sys.argv[1]

    # 从环境变量加载配置
    config = load_config_from_env()

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])
    storage.cleanup_old_news(30)

    # 执行检查
    if check_type in ["weather", "both"]:
        check_weather(config, feishu)

    if check_type in ["news", "both"]:
        check_news(config, feishu, storage)

    print("\n" + "="*60)
    print("完成")
    print("="*60)


if __name__ == "__main__":
    main()
