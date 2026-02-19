#!/usr/bin/env python3
"""
配置检查脚本 - 一键检查所有配置是否正确
"""
import json
import os
import sys


def check_file_exists(filepath: str, description: str) -> bool:
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"  ✅ {description}: {filepath}")
        return True
    else:
        print(f"  ❌ {description}: {filepath} (不存在)")
        return False


def check_config_file():
    """检查配置文件"""
    print("\n" + "="*60)
    print("1. 检查配置文件")
    print("="*60)

    if not check_file_exists("config.json", "配置文件"):
        print("\n  ⚠️ 请先创建 config.json 文件")
        print("     可以参考 config.json.example 或查看文档")
        return False

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        print("  ✅ 配置文件格式正确（JSON 有效）")
        return config
    except json.JSONDecodeError as e:
        print(f"  ❌ 配置文件格式错误: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 读取配置文件失败: {e}")
        return False


def check_tavily_config(config: dict) -> bool:
    """检查 Tavily 配置"""
    print("\n" + "="*60)
    print("2. 检查 Tavily API 配置")
    print("="*60)

    api_key = config.get("tavily_api_key", "")

    if not api_key:
        print("  ❌ 未配置 tavily_api_key")
        print("\n  📖 获取步骤：")
        print("     1. 访问 https://tavily.com")
        print("     2. 注册账号（支持 Google 登录）")
        print("     3. 复制 Dashboard 中的 API Key")
        print("     4. 填入 config.json")
        return False

    if api_key == "YOUR_TAVILY_API_KEY":
        print("  ❌ Tavily API Key 未修改（仍是占位符）")
        print("     请填入真实的 API Key")
        return False

    if not api_key.startswith("tvly-"):
        print(f"  ⚠️ API Key 格式可能不正确（应以 'tvly-' 开头）")
        print(f"     当前值: {api_key[:20]}...")
    else:
        print(f"  ✅ API Key 已配置: {api_key[:10]}...{api_key[-5:]}")

    print("\n  💡 运行 'python test_tavily.py' 可测试 API Key 是否有效")
    return True


def check_feishu_config(config: dict) -> bool:
    """检查飞书配置"""
    print("\n" + "="*60)
    print("3. 检查飞书推送配置")
    print("="*60)

    feishu = config.get("feishu", {})
    webhook_url = feishu.get("webhook_url", "")
    app_id = feishu.get("app_id", "")
    chat_id = feishu.get("chat_id", "")

    has_webhook = webhook_url and webhook_url != "YOUR_FEISHU_WEBHOOK_URL"
    has_bot = app_id and app_id != "YOUR_FEISHU_APP_ID" and chat_id

    if not has_webhook and not has_bot:
        print("  ❌ 未配置飞书推送方式")
        print("\n  📖 配置方式（二选一）：")
        print("\n  方式A - Webhook（推荐）：")
        print("     1. 打开飞书群聊")
        print("     2. 群设置 → 群机器人 → 添加机器人")
        print("     3. 选择'自定义机器人'")
        print("     4. 复制 Webhook URL")
        print("     5. 填入 config.json 的 webhook_url")
        print("\n  方式B - 飞书应用：")
        print("     1. 访问 https://open.feishu.cn/app")
        print("     2. 创建自建应用")
        print("     3. 获取 App ID、App Secret、Chat ID")
        print("     4. 填入 config.json")
        return False

    if has_webhook:
        print("  ✅ 配置方式: Webhook")
        print(f"     URL: {webhook_url[:50]}...")
        if not webhook_url.startswith("https://open.feishu.cn"):
            print("  ⚠️ Webhook URL 格式可能不正确")
            print("     标准格式: https://open.feishu.cn/open-apis/bot/v2/hook/...")

    if has_bot:
        print("  ✅ 配置方式: 飞书机器人")
        print(f"     App ID: {app_id}")
        print(f"     Chat ID: {chat_id[:20]}...")

    print("\n  💡 运行 'python test_feishu.py' 可测试飞书推送")
    return True


def check_monitoring_config(config: dict) -> bool:
    """检查监控配置"""
    print("\n" + "="*60)
    print("4. 检查监控配置")
    print("="*60)

    monitoring = config.get("monitoring", {})

    countries = monitoring.get("countries", [])
    if countries:
        print(f"  ✅ 监控国家: {', '.join(countries)}")
    else:
        print("  ⚠️ 未配置监控国家，将使用默认值")

    weather_keywords = monitoring.get("weather_keywords", [])
    if weather_keywords:
        print(f"  ✅ 天气关键词: {len(weather_keywords)} 个")
        print(f"     示例: {', '.join(weather_keywords[:3])}...")
    else:
        print("  ⚠️ 未配置天气关键词，将使用默认值")

    news_keywords = monitoring.get("news_keywords", [])
    if news_keywords:
        print(f"  ✅ 新闻关键词: {len(news_keywords)} 个")
        print(f"     示例: {', '.join(news_keywords[:3])}...")
    else:
        print("  ⚠️ 未配置新闻关键词，将使用默认值")

    weather_time = monitoring.get("weather_check_time", "08:00")
    news_time = monitoring.get("news_check_time", "09:00")
    print(f"  ✅ 天气检查时间: {weather_time}")
    print(f"  ✅ 新闻检查时间: {news_time}")

    return True


def check_storage_config(config: dict) -> bool:
    """检查存储配置"""
    print("\n" + "="*60)
    print("5. 检查存储配置")
    print("="*60)

    storage = config.get("storage", {})
    sent_news_file = storage.get("sent_news_file", "sent_news.json")

    print(f"  ✅ 新闻记录文件: {sent_news_file}")

    if os.path.exists(sent_news_file):
        try:
            with open(sent_news_file, "r") as f:
                data = json.load(f)
                news_count = len(data.get("news", []))
            print(f"  ✅ 文件存在，已记录 {news_count} 条新闻")
        except:
            print(f"  ⚠️ 文件存在但格式可能有误")
    else:
        print("  ℹ️ 文件不存在（首次运行时会自动创建）")

    max_days = storage.get("max_history_days", 30)
    print(f"  ✅ 历史记录保留: {max_days} 天")

    return True


def check_dependencies():
    """检查 Python 依赖"""
    print("\n" + "="*60)
    print("6. 检查 Python 依赖")
    print("="*60)

    required_packages = {
        "requests": "HTTP 请求库",
        "schedule": "定时任务库"
    }

    all_installed = True

    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package}: {description}")
        except ImportError:
            print(f"  ❌ {package}: 未安装")
            all_installed = False

    if not all_installed:
        print("\n  💡 运行以下命令安装缺失的依赖：")
        print("     pip install -r requirements.txt")

    return all_installed


def print_summary(checks: dict):
    """打印检查总结"""
    print("\n" + "="*60)
    print("配置检查总结")
    print("="*60)

    total = len(checks)
    passed = sum(checks.values())
    failed = total - passed

    print(f"\n  总计: {total} 项")
    print(f"  ✅ 通过: {passed} 项")
    print(f"  ❌ 失败: {failed} 项")

    if failed == 0:
        print("\n🎉 所有配置检查通过！")
        print("\n📋 下一步：")
        print("  1. 运行 'python test_tavily.py' 测试 API 连接")
        print("  2. 运行 'python test_feishu.py' 测试飞书推送")
        print("  3. 运行 'python logistics_alert.py both' 执行检查")
        print("  4. 设置 cron 定时任务")
    else:
        print("\n⚠️ 部分配置存在问题，请按照上述提示修复")
        print("\n📖 帮助文档：")
        print("  - TAVILY_SETUP.md - Tavily 注册指南")
        print("  - QUICKSTART.md - 快速开始指南")
        print("  - USAGE_GUIDE.md - 详细使用说明")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("欧洲物流预警系统 - 配置检查")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    checks = {}

    # 检查配置文件
    config = check_config_file()
    checks["config_file"] = bool(config)

    if not config:
        print_summary(checks)
        sys.exit(1)

    # 检查 Tavily
    checks["tavily"] = check_tavily_config(config)

    # 检查飞书
    checks["feishu"] = check_feishu_config(config)

    # 检查监控配置
    checks["monitoring"] = check_monitoring_config(config)

    # 检查存储配置
    checks["storage"] = check_storage_config(config)

    # 检查依赖
    checks["dependencies"] = check_dependencies()

    # 打印总结
    print_summary(checks)


if __name__ == "__main__":
    from datetime import datetime
    main()
