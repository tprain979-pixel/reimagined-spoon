#!/usr/bin/env python3
"""
欧洲物流预警系统 - 完整可执行版本
集成 Tavily API 进行实时搜索
"""
import json
import sys
import os
import requests
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


def tavily_search(api_key: str, query: str, time_range: str = "day", max_results: int = 10) -> List[Dict]:
    """
    使用 Tavily API 执行搜索

    Args:
        api_key: Tavily API Key
        query: 搜索查询
        time_range: 时间范围 (day, week, month)
        max_results: 最大结果数

    Returns:
        搜索结果列表
    """
    url = "https://api.tavily.com/search"

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_raw_content": False,
        "max_results": max_results,
        "time_range": time_range
    }

    try:
        print(f"[Tavily] 搜索: {query[:80]}...")
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        print(f"[Tavily] 找到 {len(results)} 条结果")
        return results

    except requests.exceptions.Timeout:
        print("[Tavily] ❌ 搜索超时")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[Tavily] ❌ 搜索失败: {e}")
        return []
    except Exception as e:
        print(f"[Tavily] ❌ 未知错误: {e}")
        return []


def check_weather_alerts(config: Dict, feishu: FeishuSender, tavily_key: str):
    """
    检查天气预警并推送
    """
    print(f"\n{'='*60}")
    print(f"[天气预警检查] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 获取搜索配置
    weather_config = get_weather_search_config(config)

    # 执行 Tavily 搜索
    weather_results = tavily_search(
        api_key=tavily_key,
        query=weather_config["query"],
        time_range=weather_config.get("time_range", "day"),
        max_results=weather_config.get("max_results", 10)
    )

    # 格式化报告
    report = format_weather_report(weather_results)

    # 推送到飞书（每日推送）
    if feishu.send_message(report, title="欧洲物流天气预警"):
        print("[天气预警] ✅ 推送成功")
        return True
    else:
        print("[天气预警] ❌ 推送失败")
        return False


def check_logistics_news(config: Dict, feishu: FeishuSender, storage: NewsStorage, tavily_key: str):
    """
    检查物流新闻并推送（仅推送新增）
    """
    print(f"\n{'='*60}")
    print(f"[物流新闻检查] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 获取搜索配置
    news_config = get_news_search_config(config)

    # 执行 Tavily 搜索
    news_results = tavily_search(
        api_key=tavily_key,
        query=news_config["query"],
        time_range=news_config.get("time_range", "day"),
        max_results=news_config.get("max_results", 15)
    )

    # 提取新闻条目
    all_news = extract_news_items(news_results)

    # 过滤出新增新闻
    new_news = storage.get_new_news(all_news)

    print(f"[物流新闻] 总共: {len(all_news)} 条，新增: {len(new_news)} 条")

    # 只有新增新闻时才推送
    if new_news and len(new_news) > 0:
        report = format_news_report(new_news)

        if report:
            if feishu.send_message(report, title="欧洲物流突发事件预警"):
                storage.add_sent_news(new_news)
                print("[物流新闻] ✅ 推送成功，已记录新闻")
                return True
            else:
                print("[物流新闻] ❌ 推送失败")
                return False
    else:
        print("[物流新闻] ℹ️ 没有新增新闻，跳过推送")
        return True


def main():
    """主函数"""
    print("="*60)
    print("欧洲物流预警推送系统")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 加载配置
    config = load_config()

    # 检查 Tavily API Key
    tavily_key = config.get("tavily_api_key") or os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        print("\n[错误] 未配置 Tavily API Key")
        print("请在 config.json 中添加 'tavily_api_key' 或设置环境变量 TAVILY_API_KEY")
        print("注册地址: https://tavily.com\n")
        sys.exit(1)

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 清理旧新闻记录
    storage.cleanup_old_news(config["storage"].get("max_history_days", 30))

    # 解析命令行参数
    check_type = sys.argv[1] if len(sys.argv) > 1 else "both"

    if check_type not in ["weather", "news", "both"]:
        print("用法: python logistics_alert.py [weather|news|both]")
        sys.exit(1)

    # 执行检查
    results = []

    if check_type in ["weather", "both"]:
        success = check_weather_alerts(config, feishu, tavily_key)
        results.append(("天气预警", success))

    if check_type in ["news", "both"]:
        success = check_logistics_news(config, feishu, storage, tavily_key)
        results.append(("物流新闻", success))

    # 输出汇总
    print(f"\n{'='*60}")
    print("执行汇总")
    print("="*60)
    for name, success in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"{name}: {status}")
    print("="*60)


if __name__ == "__main__":
    main()
