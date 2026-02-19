#!/usr/bin/env python3
"""
本地持续运行版本 - 适合个人电脑
只需保持程序运行即可实现定时推送
"""
import json
import sys
import os
import requests
import schedule
import time
from datetime import datetime
from typing import Dict, List

from weather_monitor import format_weather_report
from news_monitor import format_news_report, extract_news_items
from feishu_sender import FeishuSender
from storage import NewsStorage


def load_config():
    """加载配置文件"""
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        sys.exit(1)


def search_with_tavily(api_key: str, query: str, max_results: int = 10) -> List[Dict]:
    """Tavily 搜索"""
    url = "https://api.tavily.com/search"
    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "days": 1
    }

    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=data, timeout=30)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except Exception as e:
        print(f"[搜索异常] {e}")
        return []


def check_weather():
    """天气检查任务"""
    print("\n" + "="*60)
    print(f"🌤️ 天气预警检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    config = load_config()
    feishu = FeishuSender(config["feishu"])

    countries = " OR ".join(config["monitoring"]["countries"])
    keywords = " ".join(config["monitoring"]["weather_keywords"])
    query = f"({countries}) logistics transport weather {keywords}"

    results = search_with_tavily(config["tavily_api_key"], query, 10)
    report = format_weather_report(results)

    if feishu.send_message(report, title="欧洲物流天气预警"):
        print("✅ 推送成功")
    else:
        print("❌ 推送失败")


def check_news():
    """新闻检查任务"""
    print("\n" + "="*60)
    print(f"🚨 物流新闻检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    config = load_config()
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    countries = " OR ".join(config["monitoring"]["countries"])
    keywords = " OR ".join(config["monitoring"]["news_keywords"])
    query = f"({countries}) logistics ({keywords})"

    results = search_with_tavily(config["tavily_api_key"], query, 15)
    all_news = extract_news_items(results)
    new_news = storage.get_new_news(all_news)

    print(f"总共: {len(all_news)}, 新增: {len(new_news)}")

    if new_news:
        report = format_news_report(new_news)
        if report and feishu.send_message(report, title="欧洲物流突发事件预警"):
            storage.add_sent_news(new_news)
            print("✅ 推送成功")
        else:
            print("❌ 推送失败")
    else:
        print("ℹ️ 无新增，跳过")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("        欧洲物流预警推送系统 - 本地运行版本")
    print("="*70)
    print(f"\n⏰ 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📋 定时计划:")
    print("  - 天气预警: 每天 08:00 和 18:00")
    print("  - 物流新闻: 每天 09:00 和 19:00")
    print("\n💡 提示:")
    print("  - 保持此窗口运行即可实现定时推送")
    print("  - 按 Ctrl+C 可停止程序")
    print("  - 关闭窗口后程序会停止")
    print("\n" + "="*70 + "\n")

    # 设置定时任务
    schedule.every().day.at("08:00").do(check_weather)
    schedule.every().day.at("09:00").do(check_news)
    schedule.every().day.at("18:00").do(check_weather)
    schedule.every().day.at("19:00").do(check_news)

    print("✅ 定时任务已设置")
    print("\n⏳ 等待下次执行...")
    print("   (可以手动运行 logistics_alert_full.py both 立即测试)\n")

    # 显示下次执行时间
    next_run = schedule.next_run()
    if next_run:
        print(f"⏰ 下次执行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    # 运行调度循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # 每 30 秒检查一次
    except KeyboardInterrupt:
        print("\n\n👋 用户停止程序")
        print("="*70)
        sys.exit(0)


if __name__ == "__main__":
    main()
