#!/usr/bin/env python3
"""
飞书推送测试脚本
用于验证飞书配置是否正确
"""
import json
from datetime import datetime
from feishu_sender import FeishuSender


def load_config():
    """加载配置文件"""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        return None


def main():
    """测试飞书推送功能"""
    print("="*60)
    print("飞书推送功能测试")
    print("="*60)

    # 加载配置
    config = load_config()
    if not config:
        return

    # 初始化飞书发送器
    feishu = FeishuSender(config.get("feishu", {}))

    # 准备测试消息
    test_message = f"""# 系统测试消息

**测试时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

这是一条测试消息，用于验证欧洲物流预警推送系统的飞书推送功能。

## 测试内容

✅ 飞书配置正确
✅ 网络连接正常
✅ 消息格式化正常

---

如果你看到这条消息，说明系统配置成功！
"""

    # 发送测试消息
    print("\n正在发送测试消息到飞书...\n")
    success = feishu.send_message(test_message, title="系统测试")

    if success:
        print("✅ 测试成功！飞书推送功能正常工作")
    else:
        print("❌ 测试失败！请检查以下配置：")
        print("  1. config.json 中的飞书配置是否正确")
        print("  2. Webhook URL 是否有效（如果使用 webhook）")
        print("  3. App ID/Secret/Chat ID 是否正确（如果使用机器人）")
        print("  4. 网络连接是否正常")


if __name__ == "__main__":
    main()
