#!/usr/bin/env python3
"""
测试 Tavily API Key 是否有效
"""
import requests
import json
import sys


def test_tavily_api(api_key: str):
    """
    测试 Tavily API 连接

    Args:
        api_key: Tavily API Key
    """
    print("="*60)
    print("Tavily API 测试")
    print("="*60)

    if not api_key or api_key == "YOUR_TAVILY_API_KEY":
        print("\n❌ 错误：请先在 config.json 中配置 Tavily API Key")
        print("\n获取步骤：")
        print("  1. 访问 https://tavily.com")
        print("  2. 注册账号（支持 Google/GitHub 登录）")
        print("  3. 在 Dashboard 复制 API Key")
        print("  4. 填入 config.json 的 tavily_api_key 字段")
        return False

    print(f"\n🔑 API Key: {api_key[:10]}...{api_key[-5:]}")
    print(f"📍 测试查询: 'Germany logistics weather'\n")

    # 测试 API
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": api_key,
        "query": "Germany logistics weather",
        "search_depth": "basic",
        "max_results": 1
    }

    try:
        print("正在发送请求到 Tavily API...")
        response = requests.post(url, headers=headers, json=data, timeout=15)

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])

            print(f"✅ API Key 有效！")
            print(f"✅ 搜索成功，返回 {len(results)} 条结果")

            if results:
                print(f"\n📰 示例结果:")
                print(f"   标题: {results[0].get('title', '')[:60]}...")
                print(f"   URL: {results[0].get('url', '')}")

            # 显示配额信息（如果有）
            if "credits_used" in result:
                print(f"\n📊 配额使用: {result['credits_used']} credits")

            print("\n✅ Tavily API 配置正确，可以开始使用！")
            return True

        elif response.status_code == 401:
            print("❌ API Key 无效，请检查：")
            print("   1. API Key 是否复制完整")
            print("   2. 是否有多余的空格或引号")
            print("   3. 是否使用了正确的 API Key")
            return False

        elif response.status_code == 429:
            print("⚠️ API 配额已用尽")
            print("   请访问 Tavily Dashboard 查看配额情况")
            print("   或升级到付费计划")
            return False

        elif response.status_code == 433:
            print("⚠️ API 请求超过限额")
            print("   免费账号可能有每日/每月限制")
            print("   请访问 https://tavily.com 查看配额详情")
            return False

        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 网络连接失败，请检查：")
        print("   1. 是否能访问互联网")
        print("   2. 是否有代理或防火墙限制")
        return False
    except Exception as e:
        print(f"❌ 发生异常: {e}")
        return False


def main():
    """主函数"""
    # 从配置文件读取 API Key
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            api_key = config.get("tavily_api_key", "")
    except FileNotFoundError:
        print("❌ 找不到 config.json 文件")
        print("请确保在项目根目录运行此脚本")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        sys.exit(1)

    # 测试 API
    success = test_tavily_api(api_key)

    print("\n" + "="*60)
    if success:
        print("🎉 配置完成！")
        print("\n下一步：")
        print("  1. 运行 python test_feishu.py 测试飞书推送")
        print("  2. 运行 python logistics_alert.py both 执行检查")
        print("  3. 设置 cron 定时任务实现自动推送")
    else:
        print("❌ 配置失败")
        print("\n请按照提示检查配置后重试")
    print("="*60)


if __name__ == "__main__":
    main()
