"""
天气监控模块 - 监控欧洲物流相关天气预警
"""
import os
from datetime import datetime
from typing import Dict, List


def search_weather_alerts(countries: List[str] = None) -> Dict:
    """
    搜索欧洲物流相关的天气预警信息

    Args:
        countries: 要监控的国家列表，默认关注德国

    Returns:
        包含天气预警信息的字典
    """
    if countries is None:
        countries = ["Germany"]

    # 构建搜索查询
    countries_str = " OR ".join(countries)
    query = f"({countries_str}) logistics transport weather alert warning storm snow rain wind extreme temperature"

    print(f"[天气监控] 搜索查询: {query}")

    # 注意：实际搜索需要在主程序中使用 Tavily MCP 工具
    # 这里返回搜索配置
    return {
        "query": query,
        "time_range": "day",  # 最近24小时
        "max_results": 10,
        "search_type": "weather_alert"
    }


def format_weather_report(search_results: List[Dict]) -> str:
    """
    格式化天气预警报告（中英文双语）

    Args:
        search_results: Tavily 搜索返回的结果

    Returns:
        格式化的天气报告文本（中英文）
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 标题（中英文）
    report = "# 🌤️ 欧洲物流天气预警 | Europe Logistics Weather Alert\n\n"

    # 基本信息
    report += "**📅 报告时间 | Report Time:** " + timestamp + "\n"
    report += "**📍 监控区域 | Monitoring Area:** 欧洲重点国家（德国、法国、荷兰、比利时、波兰）\n"
    report += "**🔍 数据来源 | Data Source:** Tavily Real-time Search\n\n"

    report += "---\n\n"

    # 无预警情况
    if not search_results or len(search_results) == 0:
        report += "## ✅ 暂无重大天气预警 | No Major Weather Alerts\n\n"
        report += "**中文：** 今日监控区域内暂无影响物流运输的重大天气预警，运输条件正常。\n\n"
        report += "**English:** No significant weather alerts affecting logistics operations in the monitored regions today. Transport conditions are normal.\n\n"
        report += "---\n\n"
        report += "_💡 提示：系统将持续监控天气变化 | System continues to monitor weather conditions_"
        return report

    # 有预警情况 - 添加中文概览
    report += f"## 📋 今日概览\n\n"

    # 生成中文概览
    report += f"**今日监控到 {len(search_results)} 条天气预警信息。**\n\n"

    # 简要列举前3条预警
    preview_items = []
    for idx, result in enumerate(search_results[:3], 1):
        title = result.get("title", "")
        if title:
            # 提取关键信息（取前50字符）
            short_title = title[:50] + "..." if len(title) > 50 else title
            preview_items.append(f"{idx}. {short_title}")

    if preview_items:
        report += "主要预警包括：\n"
        for item in preview_items:
            report += f"- {item}\n"

    if len(search_results) > 3:
        report += f"\n还有 {len(search_results) - 3} 条其他预警，详见下方。\n"

    report += "\n**建议：** 请关注天气变化，必要时调整运输计划或路线安排。\n\n"

    report += "---\n\n"

    report += f"## ⚠️ 天气预警详情 | Weather Alert Details\n\n"
    report += f"**🔔 预警数量 | Alert Count:** {len(search_results)} 条 | {len(search_results)} alerts\n\n"
    report += "---\n\n"

    # 预警详情
    for idx, result in enumerate(search_results, 1):
        title = result.get("title", "无标题")
        url = result.get("url", "")
        content = result.get("content", "")

        # 标题
        report += f"### {idx}. {title}\n\n"

        # 内容摘要（前250字符）
        summary = content[:250].strip() + "..." if len(content) > 250 else content.strip()
        report += f"**📄 详情 | Details:**\n\n"
        report += f"{summary}\n\n"

        # 链接
        if url:
            report += f"**🔗 来源链接 | Source:** {url}\n\n"

        report += "---\n\n"

    # 底部提示
    report += "💡 **温馨提示 | Tips:**\n"
    report += "- 🚚 请关注天气变化对物流运输的影响\n"
    report += "- 🚛 Please monitor weather impacts on logistics operations\n"
    report += "- 📞 如有紧急情况请及时调整运输计划\n"
    report += "- 📱 Adjust transport plans promptly if necessary"

    return report


def get_weather_search_config(config: Dict) -> Dict:
    """
    获取天气搜索配置

    Args:
        config: 主配置字典

    Returns:
        天气搜索配置
    """
    monitoring = config.get("monitoring", {})
    countries = monitoring.get("countries", ["Germany"])

    return search_weather_alerts(countries)
