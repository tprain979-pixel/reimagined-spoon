#!/usr/bin/env python3
"""
实时演示脚本
此脚本供 Claude Code 使用，展示真实的搜索和推送功能
"""
import json
from datetime import datetime
from weather_monitor import format_weather_report
from news_monitor import format_news_report, extract_news_items
from storage import NewsStorage


def display_weather_query():
    """显示天气搜索查询"""
    query = "(Germany OR France OR Netherlands OR Belgium OR Poland) logistics transport weather alert warning storm snow rain wind extreme temperature"

    print("="*60)
    print("天气预警搜索配置")
    print("="*60)
    print(f"查询: {query}")
    print(f"时间范围: 最近1天")
    print(f"最大结果数: 10")
    print("="*60)

    return {
        "query": query,
        "time_range": "day",
        "max_results": 10
    }


def display_news_query():
    """显示新闻搜索查询"""
    query = "(Germany OR France OR Netherlands OR Belgium OR Poland) logistics (strike OR fire OR warehouse OR port closure OR transport disruption OR logistics incident OR border closure)"

    print("\n" + "="*60)
    print("物流新闻搜索配置")
    print("="*60)
    print(f"查询: {query}")
    print(f"时间范围: 最近1天")
    print(f"最大结果数: 15")
    print("="*60)

    return {
        "query": query,
        "time_range": "day",
        "max_results": 15
    }


def process_weather_results(results: list):
    """处理天气搜索结果"""
    print("\n📊 天气搜索结果统计:")
    print(f"  - 找到 {len(results)} 条结果")

    if results:
        print("\n📰 结果预览:")
        for idx, result in enumerate(results[:3], 1):
            title = result.get("title", "无标题")
            print(f"  {idx}. {title[:60]}...")

    # 格式化报告
    report = format_weather_report(results)

    print("\n" + "="*60)
    print("生成的天气报告")
    print("="*60)
    print(report)
    print("="*60)

    return report


def process_news_results(results: list, storage: NewsStorage):
    """处理新闻搜索结果"""
    print("\n📊 新闻搜索结果统计:")
    print(f"  - 找到 {len(results)} 条结果")

    # 提取新闻
    all_news = extract_news_items(results)
    new_news = storage.get_new_news(all_news)

    print(f"  - 总共: {len(all_news)} 条")
    print(f"  - 新增: {len(new_news)} 条")
    print(f"  - 已推送（跳过）: {len(all_news) - len(new_news)} 条")

    if new_news:
        print("\n🆕 新增新闻预览:")
        for idx, news in enumerate(new_news[:3], 1):
            title = news.get("title", "无标题")
            print(f"  {idx}. {title[:60]}...")

    # 格式化报告
    if new_news:
        report = format_news_report(new_news)

        print("\n" + "="*60)
        print("生成的新闻报告")
        print("="*60)
        print(report)
        print("="*60)

        # 记录这些新闻（演示模式不真实推送，但要记录）
        storage.add_sent_news(new_news)
        print("\n✅ 新闻已记录到数据库（演示模式：未推送到飞书）")

        return report
    else:
        print("\n✅ 没有新增新闻，符合预期（不推送）")
        return None


if __name__ == "__main__":
    print("\n" + "="*60)
    print("欧洲物流预警系统 - 实时演示")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    print("\n⚠️ 此脚本需要在 Claude Code 环境中运行")
    print("   Claude 将使用 Tavily MCP 工具执行真实搜索\n")

    # 初始化存储
    storage = NewsStorage("sent_news.json")

    # 显示搜索查询
    weather_query = display_weather_query()
    news_query = display_news_query()

    print("\n" + "="*60)
    print("准备就绪")
    print("="*60)
    print("\n👉 Claude 将使用以上查询参数调用 Tavily MCP 工具")
    print("👉 搜索完成后，脚本将处理结果并生成报告")
    print("\n请等待 Claude 执行搜索...\n")
