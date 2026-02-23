"""
新闻监控模块 - 监控欧洲物流相关突发事件
"""
from datetime import datetime
from typing import Dict, List, Optional


def search_logistics_news(countries: List[str] = None, keywords: List[str] = None) -> Dict:
    """
    搜索欧洲物流相关新闻（罢工、火灾、交通中断等）

    Args:
        countries: 要监控的国家列表
        keywords: 搜索关键词列表

    Returns:
        包含搜索配置的字典
    """
    if countries is None:
        countries = ["Germany", "Europe"]

    if keywords is None:
        keywords = ["strike", "fire", "warehouse", "logistics", "transport disruption"]

    # 构建搜索查询
    countries_str = " OR ".join(countries)
    keywords_str = " OR ".join(keywords)
    query = f"({countries_str}) logistics ({keywords_str})"

    print(f"[新闻监控] 搜索查询: {query}")

    return {
        "query": query,
        "time_range": "day",  # 最近24小时
        "max_results": 15,
        "search_type": "logistics_news"
    }


def format_news_report(new_news: List[Dict]) -> Optional[str]:
    """
    格式化物流新闻报告（简洁版：中文总结+链接）

    Args:
        new_news: 新增的新闻列表

    Returns:
        格式化的新闻报告文本（简洁中文总结），如果没有新新闻则返回 None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not new_news or len(new_news) == 0:
        return None

    # 标题
    report = "# 🚨 欧洲物流突发事件预警\n\n"
    report += f"**📅 报告时间：** {timestamp}\n"
    report += f"**📊 新增事件：** {len(new_news)} 条\n"
    report += f"**📍 监控区域：** 德国、法国、荷兰、比利时、波兰\n\n"
    report += "---\n\n"

    # 统计分析
    high_count = sum(1 for n in new_news if n.get("score", 0) > 0.8)
    medium_count = sum(1 for n in new_news if 0.5 < n.get("score", 0) <= 0.8)
    low_count = len(new_news) - high_count - medium_count

    # 事件类型分析
    countries_affected = set()
    event_types = {}

    for news in new_news:
        title = news.get("title", "").lower()
        content = news.get("content", "").lower()
        full_text = title + " " + content

        # 国家
        if "germany" in full_text or "german" in full_text or "hamburg" in full_text:
            countries_affected.add("德国")
        if "france" in full_text or "french" in full_text:
            countries_affected.add("法国")
        if "netherlands" in full_text or "dutch" in full_text or "rotterdam" in full_text:
            countries_affected.add("荷兰")
        if "belgium" in full_text or "belgian" in full_text:
            countries_affected.add("比利时")
        if "poland" in full_text or "polish" in full_text:
            countries_affected.add("波兰")

        # 事件类型
        if "strike" in full_text:
            event_types["罢工"] = event_types.get("罢工", 0) + 1
        if "fire" in full_text:
            event_types["火灾"] = event_types.get("火灾", 0) + 1
        if "port" in full_text or "harbour" in full_text or "harbor" in full_text:
            event_types["港口问题"] = event_types.get("港口问题", 0) + 1
        if "warehouse" in full_text:
            event_types["仓库事故"] = event_types.get("仓库事故", 0) + 1
        if "disruption" in full_text or "delay" in full_text:
            event_types["运输中断"] = event_types.get("运输中断", 0) + 1
        if "closure" in full_text or "closed" in full_text:
            event_types["关闭/封闭"] = event_types.get("关闭/封闭", 0) + 1

    # 生成中文总结
    report += "## 📋 今日总结\n\n"

    # 紧急程度
    urgency_text = []
    if high_count > 0:
        urgency_text.append(f"🔴 **{high_count} 条高紧急事件**")
    if medium_count > 0:
        urgency_text.append(f"🟡 {medium_count} 条中等紧急")
    if low_count > 0:
        urgency_text.append(f"🟢 {low_count} 条低紧急")

    report += f"**紧急程度：** {' | '.join(urgency_text)}\n\n"

    # 涉及国家
    if countries_affected:
        report += f"**涉及国家：** {' | '.join(sorted(countries_affected))}\n\n"

    # 事件类型
    if event_types:
        type_list = [f"{k}({v}条)" for k, v in sorted(event_types.items(), key=lambda x: x[1], reverse=True)]
        report += f"**事件类型：** {' | '.join(type_list)}\n\n"

    # 整体描述
    report += "**📝 情况说明：**\n\n"

    summary_parts = []

    # 按类型生成描述
    if "罢工" in event_types:
        summary_parts.append(f"监控到 {event_types['罢工']} 起罢工事件，可能影响港口和运输效率")

    if "火灾" in event_types:
        summary_parts.append(f"发生 {event_types['火灾']} 起仓库或设施火灾，相关物流节点受影响")

    if "港口问题" in event_types:
        summary_parts.append(f"{event_types['港口问题']} 个港口出现运营问题，可能导致货物延误")

    if "运输中断" in event_types or "关闭/封闭" in event_types:
        summary_parts.append("部分运输路线或设施受阻，建议寻找替代方案")

    for part in summary_parts:
        report += f"- {part}\n"

    report += "\n"

    # 行动建议
    if high_count > 0:
        report += "**⚠️ 重点建议：** 发现高紧急事件，建议：\n"
        report += "1. 立即评估对当前运输计划的影响\n"
        report += "2. 联系相关物流服务商确认情况\n"
        report += "3. 必要时启动应急预案或调整路线\n\n"
    else:
        report += "**📊 建议：** 当前事件紧急程度不高，建议持续关注事态发展，暂无需立即调整计划。\n\n"

    report += "---\n\n"

    # 详细事件列表（仅标题+链接）
    report += "## 🔗 详细事件列表\n\n"

    # 按紧急程度排序
    sorted_news = sorted(new_news, key=lambda x: x.get("score", 0), reverse=True)

    for idx, news in enumerate(sorted_news, 1):
        title = news.get("title", "无标题")
        url = news.get("url", "")
        score = news.get("score", 0)

        # 紧急程度标记
        if score > 0.8:
            urgency_icon = "🔴"
        elif score > 0.5:
            urgency_icon = "🟡"
        else:
            urgency_icon = "🟢"

        report += f"**{idx}. {urgency_icon} {title}**\n"
        if url:
            report += f"   📎 [查看详情]({url})\n"
        report += "\n"

    report += "---\n\n"
    report += "_💡 系统已记录这些事件，相同事件不会重复推送_"

    return report


def get_news_search_config(config: Dict) -> Dict:
    """
    获取新闻搜索配置

    Args:
        config: 主配置字典

    Returns:
        新闻搜索配置
    """
    monitoring = config.get("monitoring", {})
    countries = monitoring.get("countries", ["Germany"])
    keywords = monitoring.get("news_keywords", [])

    return search_logistics_news(countries, keywords)


def extract_news_items(search_results: List[Dict]) -> List[Dict]:
    """
    从搜索结果中提取新闻条目

    Args:
        search_results: Tavily 搜索返回的结果

    Returns:
        标准化的新闻条目列表
    """
    news_items = []

    for result in search_results:
        news_items.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", ""),
            "score": result.get("score", 0)
        })

    return news_items
