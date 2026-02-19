#!/usr/bin/env python3
"""
欧洲物流预警推送系统 - 完整版
直接调用 Tavily API（使用你自己的 API Key）
"""
import json
import sys
import requests
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
        print(f"[错误] 加载配置失败: {e}")
        sys.exit(1)


def search_with_tavily(api_key: str, query: str, time_range: str = "day", max_results: int = 10) -> List[Dict]:
    """
    使用 Tavily API 执行搜索

    Args:
        api_key: Tavily API Key
        query: 搜索查询
        time_range: 时间范围
        max_results: 最大结果数

    Returns:
        搜索结果列表
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_raw_content": False
    }

    # 时间范围映射
    if time_range == "day":
        data["days"] = 1
    elif time_range == "week":
        data["days"] = 7

    try:
        print(f"[Tavily] 正在搜索: {query[:60]}...")
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])
            print(f"[Tavily] ✅ 搜索成功，找到 {len(results)} 条结果")
            return results
        else:
            print(f"[Tavily] ❌ 搜索失败，状态码: {response.status_code}")
            print(f"[Tavily] 响应: {response.text}")
            return []

    except requests.exceptions.Timeout:
        print("[Tavily] ❌ 请求超时")
        return []
    except Exception as e:
        print(f"[Tavily] ❌ 搜索异常: {e}")
        return []


def check_weather(config: Dict, feishu: FeishuSender):
    """检查天气预警并推送"""
    print("\n" + "="*60)
    print(f"[天气预警] 开始检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 构建搜索查询
    countries = config["monitoring"]["countries"]
    keywords = config["monitoring"]["weather_keywords"]

    countries_str = " OR ".join(countries)
    keywords_str = " ".join(keywords)
    query = f"({countries_str}) logistics transport weather {keywords_str}"

    # 执行搜索
    api_key = config["tavily_api_key"]
    results = search_with_tavily(api_key, query, time_range="day", max_results=10)

    # 格式化报告
    report = format_weather_report(results)

    # 推送到飞书
    print("\n[天气预警] 正在推送到飞书...")
    if feishu.send_message(report, title="欧洲物流天气预警"):
        print("[天气预警] ✅ 推送成功")
    else:
        print("[天气预警] ❌ 推送失败")


def check_news(config: Dict, feishu: FeishuSender, storage: NewsStorage):
    """检查物流新闻并推送（仅新增）"""
    print("\n" + "="*60)
    print(f"[物流新闻] 开始检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 构建搜索查询
    countries = config["monitoring"]["countries"]
    keywords = config["monitoring"]["news_keywords"]

    countries_str = " OR ".join(countries)
    keywords_str = " OR ".join(keywords)
    query = f"({countries_str}) logistics ({keywords_str})"

    # 执行搜索
    api_key = config["tavily_api_key"]
    results = search_with_tavily(api_key, query, time_range="day", max_results=15)

    # 提取新闻
    all_news = extract_news_items(results)
    new_news = storage.get_new_news(all_news)

    print(f"[物流新闻] 总共: {len(all_news)} 条，新增: {len(new_news)} 条")

    # 仅在有新增时推送
    if new_news and len(new_news) > 0:
        report = format_news_report(new_news)

        if report:
            print("\n[物流新闻] 正在推送到飞书...")
            if feishu.send_message(report, title="欧洲物流突发事件预警"):
                storage.add_sent_news(new_news)
                print("[物流新闻] ✅ 推送成功，已记录新闻")
            else:
                print("[物流新闻] ❌ 推送失败")
    else:
        print("[物流新闻] ℹ️ 没有新增新闻，跳过推送")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("欧洲物流预警推送系统")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 检查命令行参数
    if len(sys.argv) < 2:
        print("\n用法:")
        print("  python logistics_alert_full.py both     # 检查天气和新闻")
        print("  python logistics_alert_full.py weather  # 仅检查天气")
        print("  python logistics_alert_full.py news     # 仅检查新闻")
        sys.exit(1)

    check_type = sys.argv[1]

    if check_type not in ["weather", "news", "both"]:
        print(f"❌ 无效的参数: {check_type}")
        print("   有效值: weather, news, both")
        sys.exit(1)

    # 加载配置
    config = load_config()

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 清理旧记录
    storage.cleanup_old_news(config["storage"].get("max_history_days", 30))

    # 执行检查
    if check_type in ["weather", "both"]:
        check_weather(config, feishu)

    if check_type in ["news", "both"]:
        check_news(config, feishu, storage)

    print("\n" + "="*60)
    print("检查完成")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
