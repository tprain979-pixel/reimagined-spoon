# 欧洲物流天气与新闻预警推送系统

自动监控欧洲（重点：德国）物流相关的天气预警和突发事件，并推送到飞书。

## 功能特性

### 1. 天气预警推送（每日推送）
- 监控欧洲物流运输相关的天气预警
- 关注：暴风雨、暴雪、极端温度、大风等影响物流的天气
- **每日定时推送**到飞书，即使没有预警也会发送报告

### 2. 物流新闻推送（增量推送）
- 监控物流相关突发事件：罢工、火灾、仓库事故、港口关闭、交通中断等
- 每日检查最新新闻
- **仅在有新增新闻时推送**，避免重复推送
- 自动去重机制，已推送的新闻不会再次推送

## 项目结构

```
logistics-alert-system/
├── config.json           # 配置文件（飞书、监控参数等）
├── main.py              # 定时任务主程序（使用 schedule 库）
├── main_with_mcp.py     # Claude Code MCP 版本
├── run_daily_check.py   # 单次执行脚本（适合 cron）
├── weather_monitor.py   # 天气监控模块
├── news_monitor.py      # 新闻监控模块
├── feishu_sender.py     # 飞书推送模块
├── storage.py           # 数据存储模块（新闻去重）
├── sent_news.json       # 已推送新闻记录
├── requirements.txt     # Python 依赖包
└── README.md           # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置文件

编辑 `config.json` 文件，填写以下信息：

#### 方式A：使用飞书 Webhook（推荐，更简单）

```json
{
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN"
  }
}
```

**获取 Webhook URL：**
1. 在飞书群聊中，点击右上角 ⚙️ → 群机器人 → 添加机器人 → 自定义机器人
2. 设置机器人名称和描述
3. 复制生成的 Webhook 地址

#### 方式B：使用飞书机器人

```json
{
  "feishu": {
    "app_id": "cli_xxxxxxxxxxxxx",
    "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxx",
    "chat_id": "oc_xxxxxxxxxxxxxxxxxxxxx"
  }
}
```

**获取机器人凭证：**
1. 访问 <a href="https://open.feishu.cn/app" target="_blank">https://open.feishu.cn/app</a> 创建企业自建应用
2. 获取 App ID 和 App Secret
3. 添加权限：`im:message`, `im:message.group_at_msg`, `im:chat`
4. 获取群聊 Chat ID：将机器人添加到群聊，使用 API 获取 chat_id

### 3. 配置监控参数

在 `config.json` 中调整监控参数：

```json
{
  "monitoring": {
    "countries": ["Germany", "France", "Netherlands", "Belgium", "Poland"],
    "weather_check_time": "08:00",
    "news_check_time": "09:00",
    "weather_keywords": ["extreme weather", "storm", "snow", "heavy rain", "transport disruption"],
    "news_keywords": ["strike", "fire", "warehouse", "port closure", "transport disruption", "logistics incident"]
  }
}
```

## 使用方法

### 方法1：定时任务模式（Python schedule）

运行主程序，会根据配置的时间自动执行检查：

```bash
python main.py
```

程序会持续运行，在指定时间自动执行检查和推送。

### 方法2：单次执行模式（适合 cron）

手动执行一次检查：

```bash
# 检查天气和新闻
python run_daily_check.py both

# 仅检查天气
python run_daily_check.py weather

# 仅检查新闻
python run_daily_check.py news
```

### 方法3：配置 Linux Cron（推荐生产环境）

编辑 crontab：

```bash
crontab -e
```

添加定时任务：

```cron
# 每天早上8点检查天气预警
0 8 * * * cd /path/to/logistics-alert-system && python run_daily_check.py weather >> logs/weather.log 2>&1

# 每天早上9点检查物流新闻
0 9 * * * cd /path/to/logistics-alert-system && python run_daily_check.py news >> logs/news.log 2>&1
```

## 重要说明

### Tavily 搜索集成

本系统依赖 Tavily 搜索 API 获取天气和新闻信息。有两种集成方式：

#### 方式A：使用 Tavily API（生产环境推荐）

1. 注册 Tavily API：<a href="https://tavily.com" target="_blank">https://tavily.com</a>
2. 在 `config.json` 添加：
   ```json
   {
     "tavily_api_key": "tvly-xxxxxxxxxxxxxxxx"
   }
   ```
3. 修改 `run_daily_check.py`，取消注释 Tavily API 调用代码

#### 方式B：在 Claude Code 环境中运行（测试推荐）

如果你有 Claude Code 环境，可以直接使用内置的 Tavily MCP 工具：
- 运行 `main_with_mcp.py`（需要在 Claude Code 对话中执行）

### 新闻去重机制

- 系统会将已推送的新闻标题和 URL 保存到 `sent_news.json`
- 每次检查时，会自动过滤掉已推送的新闻
- 只推送新增的新闻，避免重复打扰
- 默认保留30天的历史记录，可在配置中调整

## 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `feishu.webhook_url` | 飞书 Webhook 地址 | 必填（方式A） |
| `feishu.app_id` | 飞书应用 ID | 必填（方式B） |
| `feishu.app_secret` | 飞书应用密钥 | 必填（方式B） |
| `feishu.chat_id` | 飞书群聊 ID | 必填（方式B） |
| `monitoring.countries` | 监控的国家列表 | `["Germany", ...]` |
| `monitoring.weather_check_time` | 天气检查时间 | `"08:00"` |
| `monitoring.news_check_time` | 新闻检查时间 | `"09:00"` |
| `monitoring.weather_keywords` | 天气搜索关键词 | 见配置文件 |
| `monitoring.news_keywords` | 新闻搜索关键词 | 见配置文件 |
| `storage.sent_news_file` | 新闻记录文件 | `"sent_news.json"` |
| `storage.max_history_days` | 历史记录保留天数 | `30` |

## 测试

### 测试飞书推送

创建测试脚本 `test_feishu.py`：

```python
import json
from feishu_sender import FeishuSender

config = json.load(open("config.json"))
feishu = FeishuSender(config["feishu"])

test_message = "# 测试消息\n\n这是一条测试消息，用于验证飞书推送功能。"
success = feishu.send_message(test_message, title="系统测试")

print("推送成功" if success else "推送失败")
```

运行：
```bash
python test_feishu.py
```

## 故障排查

### 1. 推送失败

**检查项：**
- 飞书 Webhook URL 是否正确
- 网络连接是否正常
- 查看错误日志

### 2. 没有搜索到新闻

**可能原因：**
- 搜索关键词不够精准，调整 `config.json` 中的 keywords
- 时间范围设置问题
- Tavily API 配额用尽

### 3. 重复推送新闻

**检查项：**
- `sent_news.json` 文件是否存在并可写
- 是否有权限写入该文件
- 检查日志确认是否成功记录

## 生产部署建议

1. **使用独立服务器或容器运行**
   - 推荐使用 Docker 容器化部署
   - 确保稳定的网络环境

2. **配置日志记录**
   - 添加日志文件，便于排查问题
   - 建议使用 Python logging 模块

3. **监控和告警**
   - 监控脚本运行状态
   - 在脚本执行失败时发送告警

4. **数据备份**
   - 定期备份 `sent_news.json`
   - 避免因文件损坏导致重复推送

## 扩展功能建议

- 添加更多国家和地区的监控
- 支持多个飞书群聊推送
- 添加邮件推送备用渠道
- 提供 Web 管理界面
- 添加推送历史记录查询功能
- 根据事件严重程度分级推送

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系系统管理员。
