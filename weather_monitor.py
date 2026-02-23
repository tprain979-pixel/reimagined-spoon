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
    格式化天气预警报告（简洁版：总结+链接）

    Args:
        search_results: Tavily 搜索返回的结果

    Returns:
        格式化的天气报告文本（简洁中文总结+链接）
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 标题
    report = "# 🌤️ 欧洲物流天气预警\n\n"
    report += f"**📅 报告时间：** {timestamp}\n"
    report += f"**📍 监控区域：** 德国、法国、荷兰、比利时、波兰\n\n"
    report += "---\n\n"

    # 无预警情况
    if not search_results or len(search_results) == 0:
        report += "## ✅ 今日天气概览\n\n"
        report += "**监控区域内暂无影响物流运输的重大天气预警，运输条件正常。**\n\n"
        report += "建议继续关注天气变化，保持正常运输计划。\n\n"
        return report

    # 有预警情况 - 生成整体中文总结
    report += "## 📋 今日天气概览\n\n"

    # 统计和分类预警
    weather_summary = []
    countries_mentioned = set()
    weather_types = set()

    for result in search_results:
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        full_text = title + " " + content

        # 提取国家
        if "germany" in full_text or "german" in full_text:
            countries_mentioned.add("德国")
        if "france" in full_text or "french" in full_text:
            countries_mentioned.add("法国")
        if "netherlands" in full_text or "dutch" in full_text:
            countries_mentioned.add("荷兰")
        if "belgium" in full_text or "belgian" in full_text:
            countries_mentioned.add("比利时")
        if "poland" in full_text or "polish" in full_text:
            countries_mentioned.add("波兰")

        # 提取天气类型
        if "storm" in full_text or "风暴" in full_text:
            weather_types.add("暴风雨")
        if "snow" in full_text or "雪" in full_text:
            weather_types.add("降雪")
        if "rain" in full_text or "雨" in full_text:
            weather_types.add("降雨")
        if "wind" in full_text or "大风" in full_text:
            weather_types.add("大风")
        if "temperature" in full_text or "温度" in full_text:
            weather_types.add("极端温度")

    # 生成总结文字
    report += f"**今日监控到 {len(search_results)} 条天气预警信息。**\n\n"

    if countries_mentioned:
        report += f"**涉及国家：** {' | '.join(sorted(countries_mentioned))}\n\n"

    if weather_types:
        report += f"**天气类型：** {' | '.join(sorted(weather_types))}\n\n"

    # 主要影响总结
    report += "**主要影响：** "
    if "暴风雨" in weather_types or "大风" in weather_types:
        report += "强风可能导致运输延误和安全风险。"
    elif "降雪" in weather_types:
        report += "降雪可能影响道路通行和运输效率。"
    elif "降雨" in weather_types:
        report += "降雨可能影响物流时效。"
    else:
        report += "天气条件可能对物流运输造成一定影响。"
    report += "\n\n"

    # 行动建议
    report += "**📌 行动建议：** "
    if len(countries_mentioned) >= 3:
        report += "多个国家受影响，建议提前规划替代路线，密切关注天气发展。"
    else:
        report += "建议关注相关区域的天气变化，必要时调整运输计划。"
    report += "\n\n"

    report += "---\n\n"

    # 详细信息（仅标题+链接）
    report += "## 🔗 详细预警信息\n\n"

    for idx, result in enumerate(search_results, 1):
        title = result.get("title", "无标题")
        url = result.get("url", "")

        report += f"**{idx}.** {title}\n"
        if url:
            report += f"   📎 [查看详情]({url})\n"
        report += "\n"

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
