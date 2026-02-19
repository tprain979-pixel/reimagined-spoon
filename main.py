#!/usr/bin/env python3
"""
欧洲物流天气和新闻预警系统
每日监控天气预警和物流相关突发事件，推送到飞书
"""
import json
import os
import sys
import schedule
import time
from datetime import datetime
from typing import Dict, List

# 导入自定义模块
from weather_monitor import get_weather_search_config, format_weather_report
from news_monitor import get_news_search_config, format_news_report, extract_news_items
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


def perform_tavily_search(query: str, time_range: str = "day", max_results: int = 10) -> List[Dict]:
    """
    执行 Tavily 搜索（此函数需要手动调用 MCP 工具）

    注意：在实际使用中，需要通过 Claude Code 的 Tavily MCP 工具来执行搜索
    这里返回搜索参数供参考

    Args:
        query: 搜索查询
        time_range: 时间范围
        max_results: 最大结果数

    Returns:
        搜索结果列表
    """
    print(f"\n[搜索] 查询: {query}")
    print(f"[搜索] 时间范围: {time_range}, 最大结果数: {max_results}")
    print("[提示] 请在实际运行时通过 Tavily MCP 工具执行此搜索\n")

    # 实际使用时，这里应该调用 Tavily API 或 MCP 工具
    # 示例返回空列表
    return []


def check_weather_alerts(config: Dict, feishu: FeishuSender):
    """
    检查天气预警并推送（每日推送）
    """
    print(f"\n{'='*60}")
    print(f"[天气预警检查] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 获取搜索配置
    search_config = get_weather_search_config(config)

    # 提示：实际使用时需要通过 Tavily MCP 执行搜索
    print("[提示] 实际部署时，请使用以下参数调用 Tavily 搜索：")
    print(f"  - query: {search_config['query']}")
    print(f"  - time_range: {search_config['time_range']}")
    print(f"  - max_results: {search_config['max_results']}")

    # 模拟搜索结果（实际使用时替换为真实搜索）
    search_results = perform_tavily_search(
        query=search_config["query"],
        time_range=search_config.get("time_range", "day"),
        max_results=search_config.get("max_results", 10)
    )

    # 格式化报告
    report = format_weather_report(search_results)

    # 推送到飞书（每日推送，即使没有预警）
    success = feishu.send_message(report, title="欧洲物流天气预警")

    if success:
        print("[天气预警] ✅ 推送成功")
    else:
        print("[天气预警] ❌ 推送失败")


def check_logistics_news(config: Dict, feishu: FeishuSender, storage: NewsStorage):
    """
    检查物流新闻并推送（仅推送新增新闻）
    """
    print(f"\n{'='*60}")
    print(f"[物流新闻检查] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 获取搜索配置
    search_config = get_news_search_config(config)

    # 提示：实际使用时需要通过 Tavily MCP 执行搜索
    print("[提示] 实际部署时，请使用以下参数调用 Tavily 搜索：")
    print(f"  - query: {search_config['query']}")
    print(f"  - time_range: {search_config['time_range']}")
    print(f"  - max_results: {search_config['max_results']}")

    # 模拟搜索结果（实际使用时替换为真实搜索）
    search_results = perform_tavily_search(
        query=search_config["query"],
        time_range=search_config.get("time_range", "day"),
        max_results=search_config.get("max_results", 15)
    )

    # 提取新闻条目
    all_news = extract_news_items(search_results)

    # 过滤出新增新闻
    new_news = storage.get_new_news(all_news)

    print(f"[物流新闻] 总共检查: {len(all_news)} 条，新增: {len(new_news)} 条")

    # 只有新增新闻时才推送
    if new_news and len(new_news) > 0:
        report = format_news_report(new_news)

        if report:
            success = feishu.send_message(report, title="欧洲物流突发事件预警")

            if success:
                # 推送成功后，记录这些新闻
                storage.add_sent_news(new_news)
                print("[物流新闻] ✅ 推送成功，已记录新闻")
            else:
                print("[物流新闻] ❌ 推送失败")
    else:
        print("[物流新闻] ℹ️ 没有新增新闻，跳过推送")


def run_scheduled_tasks(config: Dict):
    """
    运行定时任务
    """
    print("[启动] 物流预警推送系统")
    print(f"[配置] 天气检查时间: {config['monitoring']['weather_check_time']}")
    print(f"[配置] 新闻检查时间: {config['monitoring']['news_check_time']}")
    print(f"[配置] 监控国家: {', '.join(config['monitoring']['countries'])}")

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 清理旧新闻记录
    max_history_days = config["storage"].get("max_history_days", 30)
    storage.cleanup_old_news(max_history_days)

    # 设置定时任务
    weather_time = config["monitoring"]["weather_check_time"]
    news_time = config["monitoring"]["news_check_time"]

    schedule.every().day.at(weather_time).do(
        check_weather_alerts, config=config, feishu=feishu
    )

    schedule.every().day.at(news_time).do(
        check_logistics_news, config=config, feishu=feishu, storage=storage
    )

    print(f"\n[就绪] 定时任务已设置")
    print(f"  - 天气预警: 每天 {weather_time}")
    print(f"  - 新闻监控: 每天 {news_time}\n")

    # 运行任务调度循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\n[停止] 用户中断程序")
        sys.exit(0)


def run_manual_check(config: Dict):
    """
    手动执行一次检查（用于测试）
    """
    print("[手动检查] 开始执行...\n")

    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 执行天气检查
    check_weather_alerts(config, feishu)

    # 执行新闻检查
    check_logistics_news(config, feishu, storage)

    print("\n[手动检查] 完成")


def main():
    """主函数"""
    # 加载配置
    config = load_config()

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        # 手动检查模式（用于测试）
        run_manual_check(config)
    else:
        # 定时任务模式
        run_scheduled_tasks(config)


if __name__ == "__main__":
    main()
