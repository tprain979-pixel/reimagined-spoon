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
    格式化物流新闻报告（中英文双语，仅包含新增新闻）

    Args:
        new_news: 新增的新闻列表

    Returns:
        格式化的新闻报告文本，如果没有新新闻则返回 None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not new_news or len(new_news) == 0:
        # 如果没有新新闻，返回 None 表示不需要推送
        return None

    # 标题（中英文）
    report = "# 🚨 欧洲物流突发事件预警 | Europe Logistics Incident Alert\n\n"

    # 基本信息
    report += "**📅 报告时间 | Report Time:** " + timestamp + "\n"
    report += "**📊 新增事件 | New Incidents:** " + str(len(new_news)) + " 条 | " + str(len(new_news)) + " alerts\n"
    report += "**📍 监控区域 | Monitoring Area:** 德国、法国、荷兰、比利时、波兰 | Germany, France, Netherlands, Belgium, Poland\n"
    report += "**🔍 数据来源 | Data Source:** Tavily Real-time Search (Past 24 hours)\n\n"

    report += "---\n\n"

    # 添加中文概览
    report += "## 📋 今日概览\n\n"

    # 统计紧急程度
    high_count = sum(1 for n in new_news if n.get("score", 0) > 0.8)
    medium_count = sum(1 for n in new_news if 0.5 < n.get("score", 0) <= 0.8)
    low_count = len(new_news) - high_count - medium_count

    # 生成概览文字
    report += f"**过去24小时内新增 {len(new_news)} 条物流突发事件。**\n\n"

    # 紧急程度统计
    urgency_parts = []
    if high_count > 0:
        urgency_parts.append(f"🔴 高紧急 {high_count} 条")
    if medium_count > 0:
        urgency_parts.append(f"🟡 中等 {medium_count} 条")
    if low_count > 0:
        urgency_parts.append(f"🟢 低紧急 {low_count} 条")

    if urgency_parts:
        report += f"**紧急程度分布：** {' | '.join(urgency_parts)}\n\n"

    # 事件类型分析（基于标题关键词）
    event_types = []
    titles_text = " ".join([n.get("title", "").lower() for n in new_news])

    if "strike" in titles_text or "罢工" in titles_text:
        event_types.append("罢工")
    if "fire" in titles_text or "火灾" in titles_text:
        event_types.append("火灾")
    if "port" in titles_text or "港口" in titles_text:
        event_types.append("港口问题")
    if "warehouse" in titles_text or "仓库" in titles_text:
        event_types.append("仓库问题")
    if "disruption" in titles_text or "中断" in titles_text:
        event_types.append("运输中断")

    if event_types:
        report += f"**涉及类型：** {' | '.join(event_types)}\n\n"

    # 行动建议
    if high_count > 0:
        report += "**⚠️ 重点关注：** 发现高紧急事件，建议立即评估对物流的影响并采取应对措施。\n\n"
    else:
        report += "**📊 情况评估：** 当前事件紧急程度较低，建议持续关注事态发展。\n\n"

    report += "---\n\n"

    report += "## ⚠️ 新增事件详情 | New Incident Details\n\n"
    report += "**⚡ 中文：** 以下为过去24小时内新增的物流相关事件，请注意关注\n"
    report += "**⚡ English:** Following incidents occurred in the past 24 hours, please pay attention\n\n"

    # 事件详情
    for idx, news in enumerate(new_news, 1):
        title = news.get("title", "无标题")
        url = news.get("url", "")
        content = news.get("content", "")
        score = news.get("score", 0)

        # 根据相关性分数判断重要程度
        if score > 0.8:
            urgency_cn = "🔴 高"
            urgency_en = "🔴 High"
        elif score > 0.5:
            urgency_cn = "🟡 中"
            urgency_en = "🟡 Medium"
        else:
            urgency_cn = "🟢 低"
            urgency_en = "🟢 Low"

        # 事件标题
        report += f"### 📰 {idx}. {title}\n\n"

        # 紧急程度（双语）
        report += f"**⚡ 紧急程度 | Urgency:** {urgency_cn} | {urgency_en}\n\n"

        # 内容摘要（前280字符）
        summary = content[:280].strip() + "..." if len(content) > 280 else content.strip()
        report += f"**📋 事件描述 | Description:**\n\n"
        report += f"{summary}\n\n"

        # 链接
        if url:
            report += f"**🔗 详情链接 | Source:** {url}\n\n"

        report += "---\n\n"

    # 底部提示
    report += "💡 **重要提示 | Important Notes:**\n\n"
    report += "✅ **中文：** 系统已记录这些事件，相同事件不会重复推送\n\n"
    report += "✅ **English:** These incidents have been recorded and will not be pushed repeatedly\n\n"
    report += "📞 **中文：** 如遇影响请及时调整物流计划或联系相关部门\n\n"
    report += "📱 **English:** Please adjust logistics plans or contact relevant departments if affected"

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
