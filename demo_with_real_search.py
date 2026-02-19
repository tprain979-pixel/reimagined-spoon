#!/usr/bin/env python3
"""
完整演示脚本 - 使用真实的 Tavily 搜索
展示系统如何工作（需要配置 Tavily API Key）
"""
import json
import sys
import os
from datetime import datetime

# 导入自定义模块
from weather_monitor import format_weather_report, get_weather_search_config
from news_monitor import format_news_report, extract_news_items, get_news_search_config
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


def print_section(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")


def demo_weather_check(send_to_feishu: bool = False):
    """
    演示天气预警检查
    """
    print_section("演示 1: 天气预警检查（每日推送）")

    config = load_config()

    print("📍 监控配置:")
    print(f"  - 国家: {', '.join(config['monitoring']['countries'])}")
    print(f"  - 关键词: {', '.join(config['monitoring']['weather_keywords'][:3])} ...")

    # 获取搜索配置
    weather_config = get_weather_search_config(config)
    print(f"\n🔍 搜索查询: {weather_config['query'][:80]}...")

    # 模拟搜索结果
    print("\n⚠️ 注意：这是模拟结果。实际使用需要 Tavily API Key")
    print("   演示使用模拟数据展示系统功能\n")

    mock_results = [
        {
            "title": "Storm Alerts Issued Across Germany - Transport Delays Expected",
            "url": "https://example.com/weather/storm-germany",
            "content": "Severe storm warnings have been issued for northern Germany. Transport authorities warn of potential delays in logistics operations due to high winds and heavy rainfall. Highway closures possible.",
            "score": 0.85
        },
        {
            "title": "Heavy Snowfall Expected in Poland - Logistics Networks on Alert",
            "url": "https://example.com/weather/snow-poland",
            "content": "Weather services predict heavy snowfall across Poland this week. Logistics companies are preparing contingency plans as road conditions may deteriorate significantly.",
            "score": 0.78
        }
    ]

    # 格式化报告
    report = format_weather_report(mock_results)

    print("📄 生成的天气报告预览：")
    print("-" * 60)
    print(report)
    print("-" * 60)

    # 可选：发送到飞书
    if send_to_feishu:
        print("\n📤 正在推送到飞书...")
        feishu = FeishuSender(config["feishu"])
        if feishu.send_message(report, title="欧洲物流天气预警"):
            print("✅ 推送成功！请查看飞书群聊")
        else:
            print("❌ 推送失败，请检查飞书配置")
    else:
        print("\n💡 提示：使用 --send 参数可推送到飞书")


def demo_news_check(send_to_feishu: bool = False):
    """
    演示物流新闻检查（仅推送新增）
    """
    print_section("演示 2: 物流新闻检查（增量推送）")

    config = load_config()
    storage = NewsStorage(config["storage"]["sent_news_file"])

    print("📍 监控配置:")
    print(f"  - 国家: {', '.join(config['monitoring']['countries'])}")
    print(f"  - 关键词: {', '.join(config['monitoring']['news_keywords'][:3])} ...")

    # 获取搜索配置
    news_config = get_news_search_config(config)
    print(f"\n🔍 搜索查询: {news_config['query'][:80]}...")

    print("\n⚠️ 注意：这是模拟结果。实际使用需要 Tavily API Key\n")

    # 模拟搜索结果
    mock_results = [
        {
            "title": "Major Strike at Hamburg Port - Shipping Delays Expected",
            "url": "https://example.com/news/hamburg-strike",
            "content": "Workers at Hamburg port have initiated a strike demanding better wages. The strike affects major shipping operations and may cause significant delays in European logistics networks. Container handling has been reduced by 60%.",
            "score": 0.92
        },
        {
            "title": "Warehouse Fire in Netherlands Disrupts Distribution Network",
            "url": "https://example.com/news/warehouse-fire-nl",
            "content": "A major warehouse fire in Rotterdam has disrupted logistics operations. The facility, which handles distribution for several major retailers, is expected to be offline for several weeks while damage is assessed.",
            "score": 0.87
        },
        {
            "title": "Belgium Transport Strike Enters Third Day",
            "url": "https://example.com/news/belgium-transport",
            "content": "Transport workers in Belgium continue their strike for the third consecutive day. Major highways and rail routes are affected, causing delays in cross-border logistics.",
            "score": 0.81
        }
    ]

    # 提取新闻
    all_news = extract_news_items(mock_results)
    print(f"📰 搜索到: {len(all_news)} 条新闻")

    # 检查去重
    new_news = storage.get_new_news(all_news)
    print(f"🆕 新增新闻: {len(new_news)} 条")
    print(f"♻️ 已推送（跳过）: {len(all_news) - len(new_news)} 条")

    if new_news and len(new_news) > 0:
        report = format_news_report(new_news)

        print("\n📄 生成的新闻报告预览：")
        print("-" * 60)
        print(report)
        print("-" * 60)

        # 可选：发送到飞书
        if send_to_feishu:
            print("\n📤 正在推送到飞书...")
            feishu = FeishuSender(config["feishu"])
            if feishu.send_message(report, title="欧洲物流突发事件预警"):
                # 记录已推送
                storage.add_sent_news(new_news)
                print("✅ 推送成功！新闻已记录到数据库")
            else:
                print("❌ 推送失败，请检查飞书配置")
        else:
            print("\n💡 提示：使用 --send 参数可推送到飞书")
            print("💡 提示：新闻已记录，下次运行将被视为已推送")
            # 即使不推送，也记录这些新闻（避免演示多次推送）
            storage.add_sent_news(new_news)
    else:
        print("\n✅ 没有新增新闻，系统不会推送")
        print("（这符合预期：只在有新事件时才推送）")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("欧洲物流预警推送系统 - 功能演示")
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 检查是否要推送到飞书
    send_to_feishu = "--send" in sys.argv

    if send_to_feishu:
        print("\n📤 将推送消息到飞书")
    else:
        print("\n👀 仅预览模式（不推送到飞书）")
        print("   使用 --send 参数可推送到飞书")

    # 演示天气检查
    demo_weather_check(send_to_feishu)

    # 演示新闻检查
    demo_news_check(send_to_feishu)

    # 总结
    print_section("演示总结")
    print("✅ 天气预警功能：每日推送，无论是否有预警")
    print("✅ 物流新闻功能：仅在有新增新闻时推送，自动去重")
    print("\n📖 下一步：")
    print("  1. 配置 Tavily API Key（注册: https://tavily.com）")
    print("  2. 配置飞书 Webhook（在群聊中添加机器人）")
    print("  3. 运行 python test_feishu.py 测试推送")
    print("  4. 运行 python logistics_alert.py both 执行真实检查")
    print("  5. 设置 cron 定时任务实现每日自动推送")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
