#!/usr/bin/env python3
"""
每日检查脚本 - 实际执行天气和新闻检查并推送到飞书
适用于 cron 定时任务或手动执行
"""
import json
import sys
import os
from datetime import datetime
from typing import Dict, List

# 导入自定义模块
from weather_monitor import format_weather_report, get_weather_search_config
from news_monitor import format_news_report, extract_news_items, get_news_search_config
from feishu_sender import FeishuSender
from storage import NewsStorage


def load_config(config_file: str = "config.json") -> Dict:
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[错误] 加载配置文件失败: {e}")
        sys.exit(1)


def main(check_type: str = "both"):
    """
    主函数

    Args:
        check_type: 检查类型 - "weather"（仅天气）, "news"（仅新闻）, "both"（都检查）
    """
    print("="*60)
    print(f"欧洲物流预警系统 - 每日检查")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"检查类型: {check_type}")
    print("="*60)

    # 加载配置
    config = load_config()

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 清理旧新闻记录
    storage.cleanup_old_news(config["storage"].get("max_history_days", 30))

    # ========== 天气预警检查 ==========
    if check_type in ["weather", "both"]:
        print("\n[1/2] 检查天气预警...")

        weather_config = get_weather_search_config(config)

        print(f"\n⚠️ 注意：此脚本需要集成 Tavily API")
        print(f"搜索参数：")
        print(f"  - Query: {weather_config['query']}")
        print(f"  - Time Range: {weather_config['time_range']}")
        print(f"  - Max Results: {weather_config['max_results']}")
        print(f"\n请在实际部署时：")
        print(f"  1. 注册 Tavily API (https://tavily.com)")
        print(f"  2. 在配置文件中添加 TAVILY_API_KEY")
        print(f"  3. 取消注释下方的搜索代码\n")

        # TODO: 取消注释以启用实际搜索
        # import requests
        # tavily_key = config.get("tavily_api_key")
        # response = requests.post(
        #     "https://api.tavily.com/search",
        #     json={
        #         "api_key": tavily_key,
        #         "query": weather_config["query"],
        #         "search_depth": "basic",
        #         "max_results": weather_config["max_results"]
        #     }
        # )
        # weather_results = response.json().get("results", [])

        # 示例：使用空结果（实际部署时替换）
        weather_results = []
        weather_report = format_weather_report(weather_results)

        # 推送到飞书
        if feishu.send_message(weather_report, title="欧洲物流天气预警"):
            print("[天气预警] ✅ 推送成功")
        else:
            print("[天气预警] ❌ 推送失败")

    # ========== 物流新闻检查 ==========
    if check_type in ["news", "both"]:
        print("\n[2/2] 检查物流新闻...")

        news_config = get_news_search_config(config)

        print(f"\n搜索参数：")
        print(f"  - Query: {news_config['query']}")
        print(f"  - Time Range: {news_config['time_range']}")
        print(f"  - Max Results: {news_config['max_results']}\n")

        # TODO: 取消注释以启用实际搜索
        # news_results = []  # 替换为实际 Tavily API 调用

        # 示例：使用空结果
        news_results = []
        all_news = extract_news_items(news_results)
        new_news = storage.get_new_news(all_news)

        print(f"[物流新闻] 总共检查: {len(all_news)} 条，新增: {len(new_news)} 条")

        if new_news and len(new_news) > 0:
            news_report = format_news_report(new_news)

            if news_report:
                if feishu.send_message(news_report, title="欧洲物流突发事件预警"):
                    storage.add_sent_news(new_news)
                    print("[物流新闻] ✅ 推送成功，已记录新闻")
                else:
                    print("[物流新闻] ❌ 推送失败")
        else:
            print("[物流新闻] ℹ️ 没有新增新闻，跳过推送")

    print("\n" + "="*60)
    print("检查完成")
    print("="*60)


if __name__ == "__main__":
    # 支持命令行参数指定检查类型
    check_type = sys.argv[1] if len(sys.argv) > 1 else "both"

    if check_type not in ["weather", "news", "both"]:
        print("用法: python run_daily_check.py [weather|news|both]")
        sys.exit(1)

    main(check_type)
