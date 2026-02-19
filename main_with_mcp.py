#!/usr/bin/env python3
"""
欧洲物流天气和新闻预警系统（使用 Tavily MCP 版本）
这个版本需要在 Claude Code 环境中运行，直接调用 Tavily MCP 工具
"""
import json
import os
from datetime import datetime
from typing import Dict, List

# 导入自定义模块
from weather_monitor import format_weather_report
from news_monitor import format_news_report, extract_news_items
from feishu_sender import FeishuSender
from storage import NewsStorage


def load_config(config_file: str = "config.json") -> Dict:
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[错误] 加载配置文件失败: {e}")
        return None


def run_weather_check(config: Dict, search_results: List[Dict]) -> Dict:
    """
    执行天气预警检查

    Args:
        config: 配置字典
        search_results: Tavily 搜索结果

    Returns:
        包含报告内容的字典
    """
    print(f"\n{'='*60}")
    print(f"[天气预警检查] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 格式化报告
    report = format_weather_report(search_results)

    return {
        "report": report,
        "title": "欧洲物流天气预警",
        "should_send": True  # 天气预警每日推送
    }


def run_news_check(config: Dict, search_results: List[Dict], storage: NewsStorage) -> Dict:
    """
    执行物流新闻检查

    Args:
        config: 配置字典
        search_results: Tavily 搜索结果
        storage: 新闻存储对象

    Returns:
        包含报告内容的字典
    """
    print(f"\n{'='*60}")
    print(f"[物流新闻检查] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 提取新闻条目
    all_news = extract_news_items(search_results)

    # 过滤出新增新闻
    new_news = storage.get_new_news(all_news)

    print(f"[物流新闻] 总共检查: {len(all_news)} 条，新增: {len(new_news)} 条")

    # 只有新增新闻时才推送
    if new_news and len(new_news) > 0:
        report = format_news_report(new_news)
        return {
            "report": report,
            "title": "欧洲物流突发事件预警",
            "should_send": True,
            "new_news": new_news
        }
    else:
        print("[物流新闻] ℹ️ 没有新增新闻，跳过推送")
        return {
            "report": None,
            "title": "欧洲物流突发事件预警",
            "should_send": False,
            "new_news": []
        }


def send_to_feishu(feishu: FeishuSender, report_data: Dict, storage: NewsStorage = None):
    """
    发送报告到飞书

    Args:
        feishu: 飞书发送器对象
        report_data: 报告数据字典
        storage: 新闻存储对象（用于新闻推送成功后记录）
    """
    if not report_data.get("should_send"):
        print(f"[{report_data['title']}] 无需推送")
        return

    report = report_data.get("report")
    title = report_data.get("title")

    if not report:
        print(f"[{title}] 报告内容为空，跳过推送")
        return

    success = feishu.send_message(report, title=title)

    if success:
        print(f"[{title}] ✅ 推送成功")

        # 如果是新闻推送且成功，记录这些新闻
        if storage and "new_news" in report_data:
            storage.add_sent_news(report_data["new_news"])
            print(f"[{title}] 已记录 {len(report_data['new_news'])} 条新闻")
    else:
        print(f"[{title}] ❌ 推送失败")


def main():
    """
    主函数 - 执行一次完整检查
    在实际使用中，你需要通过外部调度工具（如 cron）每日定时运行此脚本
    """
    print("[启动] 欧洲物流预警推送系统")
    print(f"[时间] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 加载配置
    config = load_config()
    if not config:
        print("[错误] 无法加载配置文件，退出")
        return

    # 初始化组件
    feishu = FeishuSender(config["feishu"])
    storage = NewsStorage(config["storage"]["sent_news_file"])

    # 清理旧新闻记录
    max_history_days = config["storage"].get("max_history_days", 30)
    storage.cleanup_old_news(max_history_days)

    print("[提示] 此脚本需要在 Claude Code 环境中运行")
    print("[提示] 因为它依赖 Tavily MCP 工具进行实时搜索")
    print("[提示] 请参考 README.md 了解如何配置和使用\n")

    # 在实际使用中，这里需要调用 Tavily MCP 工具
    # 示例代码如下（需要在 Claude Code 中执行）：
    """
    # 1. 天气预警搜索
    weather_config = get_weather_search_config(config)
    weather_results = mcp__tavily__tavily_search(
        query=weather_config["query"],
        time_range=weather_config["time_range"],
        max_results=weather_config["max_results"]
    )

    # 2. 物流新闻搜索
    news_config = get_news_search_config(config)
    news_results = mcp__tavily__tavily_search(
        query=news_config["query"],
        time_range=news_config["time_range"],
        max_results=news_config["max_results"]
    )

    # 3. 处理并推送结果
    weather_report = run_weather_check(config, weather_results)
    send_to_feishu(feishu, weather_report)

    news_report = run_news_check(config, news_results, storage)
    send_to_feishu(feishu, news_report, storage)
    """

    print("[完成] 检查完成")


if __name__ == "__main__":
    main()
