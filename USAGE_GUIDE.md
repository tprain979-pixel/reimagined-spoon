# 使用指南 - 欧洲物流预警推送系统

## 系统简介

这是一个自动化的物流预警系统，用于监控欧洲（特别是德国）的：
1. **天气预警** - 每日推送到飞书
2. **物流突发事件** - 仅在有新增事件时推送（自动去重）

## 核心特性对比

| 功能 | 天气预警 | 物流新闻 |
|------|---------|---------|
| 推送频率 | 每日推送 | 增量推送 |
| 无内容时 | 仍然推送"暂无预警" | 不推送 |
| 去重机制 | ❌ 不需要 | ✅ 自动去重 |
| 监控内容 | 暴风雨、暴雪、极端温度 | 罢工、火灾、交通中断 |

## 5分钟快速配置

### 步骤 1：获取 Tavily API Key

1. 访问 <a href="https://tavily.com" target="_blank">https://tavily.com</a>
2. 注册账号（支持 Google 登录）
3. 进入 Dashboard 获取 API Key
4. 复制你的密钥（格式：`tvly-xxxxxxxxxx`）

**免费额度：** Tavily 提供免费试用额度，足够日常使用。

### 步骤 2：配置飞书机器人

#### 方式A：Webhook（推荐，最简单）

1. 打开飞书群聊
2. 点击右上角 ⚙️ → 群机器人 → 添加机器人
3. 选择 "自定义机器人"
4. 设置名称：`物流预警机器人`
5. 安全设置：可选择 "签名校验" 或不设置
6. 复制生成的 Webhook URL

#### 方式B：飞书应用（高级用户）

如需更多控制（如@指定人、发送图片等），可创建飞书应用：
1. 访问 <a href="https://open.feishu.cn/app" target="_blank">https://open.feishu.cn/app</a>
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 添加权限：`im:message`, `im:message.group_at_msg`
5. 将机器人添加到群聊并获取 Chat ID

### 步骤 3：编辑配置文件

打开 `config.json`，填入你的密钥：

```json
{
  "tavily_api_key": "tvly-你的密钥",
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的token"
  }
}
```

### 步骤 4：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 5：测试运行

```bash
# 测试飞书推送
python test_feishu.py

# 运行功能演示（不推送）
python demo_with_real_search.py

# 运行功能演示（推送到飞书）
python demo_with_real_search.py --send

# 执行真实检查并推送
python logistics_alert.py both
```

## 设置定时任务

### Linux/Mac - 使用 Cron

```bash
# 编辑 crontab
crontab -e

# 添加以下行（修改为你的实际路径）
0 8 * * * cd /你的路径/logistics-alert-system && /usr/bin/python3 logistics_alert.py weather >> logs/weather.log 2>&1
0 9 * * * cd /你的路径/logistics-alert-system && /usr/bin/python3 logistics_alert.py news >> logs/news.log 2>&1
```

**说明：**
- `0 8 * * *` = 每天早上 8:00
- `0 9 * * *` = 每天早上 9:00
- `>> logs/weather.log 2>&1` = 保存日志到文件

### Windows - 使用任务计划程序

1. 打开 "任务计划程序"（Win + R → taskschd.msc）
2. 创建基本任务
3. 设置触发器：每天早上 8:00 和 9:00
4. 操作：启动程序
   - 程序：`C:\Python\python.exe`
   - 参数：`logistics_alert.py weather`
   - 起始于：`C:\你的路径\logistics-alert-system`

### Docker - 容器化部署

```bash
# 构建镜像
docker build -t logistics-alert .

# 运行容器（手动执行）
docker run --rm \
  -e TAVILY_API_KEY=你的key \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/sent_news.json:/app/sent_news.json \
  logistics-alert both

# 配合 cron 使用
0 8 * * * docker run --rm -e TAVILY_API_KEY=xxx -v /path/config.json:/app/config.json logistics-alert weather
0 9 * * * docker run --rm -e TAVILY_API_KEY=xxx -v /path/config.json:/app/config.json -v /path/sent_news.json:/app/sent_news.json logistics-alert news
```

## 日常使用

### 手动执行检查

```bash
# 检查天气和新闻
python logistics_alert.py both

# 仅检查天气预警
python logistics_alert.py weather

# 仅检查物流新闻
python logistics_alert.py news
```

### 查看已推送的新闻

```bash
# 查看新闻记录
cat sent_news.json

# 或使用 Python 美化输出
python -m json.tool sent_news.json
```

### 清除历史记录（重新推送所有新闻）

```bash
# 备份
cp sent_news.json sent_news.backup.json

# 清空记录
echo '{"news": []}' > sent_news.json
```

## 自定义配置

### 调整监控国家

编辑 `config.json`：

```json
{
  "monitoring": {
    "countries": ["Germany", "Austria", "Switzerland", "Denmark"]
  }
}
```

### 添加搜索关键词

```json
{
  "monitoring": {
    "weather_keywords": ["hurricane", "flood", "ice storm", "blizzard"],
    "news_keywords": ["accident", "customs delay", "road closure", "rail strike"]
  }
}
```

### 修改推送时间

```json
{
  "monitoring": {
    "weather_check_time": "07:30",
    "news_check_time": "18:00"
  }
}
```

### 调整历史记录保留时长

```json
{
  "storage": {
    "max_history_days": 60
  }
}
```

## 推送消息示例

### 天气预警消息示例

```
# 欧洲物流天气预警报告

**报告时间:** 2026-02-19 08:00:00
**监控区域:** 欧洲（重点：德国）

⚠️ **发现 2 条天气预警信息**

## 1. Storm Alerts Issued Across Germany - Transport Delays Expected

Severe storm warnings have been issued for northern Germany...

**来源:** https://example.com/weather/...

---

## 2. Heavy Snowfall Expected in Poland - Logistics Networks on Alert

Weather services predict heavy snowfall across Poland...
```

### 物流新闻消息示例

```
# 欧洲物流突发事件预警

**报告时间:** 2026-02-19 09:00:00
**新增事件:** 2 条

🚨 **以下为新增物流相关事件，请注意关注**

## 1. Major Strike at Hamburg Port - Shipping Delays Expected

**紧急程度:** 🔴 高

Workers at Hamburg port have initiated a strike...

**详情链接:** https://example.com/news/...

---

_系统已记录这些新闻，不会重复推送_
```

## 常见问题

### Q1: 为什么天气预警每天都推送？

因为天气预警需要每日关注。即使当天没有重大预警，也会推送"暂无重大天气预警"的消息，让你知道系统正常运行。

### Q2: 物流新闻会推送历史新闻吗？

不会。系统会将已推送的新闻记录到 `sent_news.json`，相同新闻不会重复推送。只有新增的事件才会推送。

### Q3: 如何避免漏掉重要新闻？

系统每天检查最近24小时的新闻，并且保留30天的历史记录。只要新闻在这个时间范围内出现，就不会漏掉。

### Q4: Tavily API 费用如何？

Tavily 提供免费试用额度。每天2次搜索（天气+新闻），月度使用量很低。具体定价请查看官网。

### Q5: 可以推送到多个飞书群吗？

当前版本支持单个群聊。如需多群推送，可以：
- 配置多个 webhook_url 数组
- 修改 `feishu_sender.py` 支持批量推送

### Q6: 如何监控脚本是否正常运行？

建议：
1. 在 cron 中配置日志输出：`>> logs/cron.log 2>&1`
2. 定期检查日志文件
3. 配置飞书机器人，在脚本执行失败时发送告警

### Q7: 搜索结果不准确怎么办？

调整 `config.json` 中的搜索关键词：
- 添加更多相关关键词
- 移除不相关的关键词
- 调整国家范围

## 部署架构建议

### 小规模（个人/小团队）

**推荐：** Linux 服务器 + Cron

```
[Linux 服务器]
    ├── Cron Job (8:00) → 天气检查
    ├── Cron Job (9:00) → 新闻检查
    └── 推送到飞书群
```

### 中等规模（多团队）

**推荐：** Docker + 编排工具

```
[Docker 容器]
    ├── 定时任务容器
    ├── 配置文件挂载
    └── 数据持久化卷
```

### 大规模（企业级）

**推荐：** 云函数 + 定时触发器

```
[阿里云函数计算 / AWS Lambda]
    ├── 定时触发器（CloudWatch / 阿里云定时触发）
    ├── 函数代码打包部署
    └── 环境变量配置
```

## 监控和维护

### 日志查看

```bash
# 查看最近的日志
tail -f logs/weather.log
tail -f logs/news.log

# 查看特定日期的日志
grep "2026-02-19" logs/*.log
```

### 健康检查

每周检查：
1. ✅ Cron 任务是否正常运行
2. ✅ 日志文件是否有错误
3. ✅ 飞书消息是否正常收到
4. ✅ `sent_news.json` 文件大小是否合理（不应过大）

### 数据维护

```bash
# 每月清理旧日志
find logs/ -name "*.log" -mtime +30 -delete

# 查看新闻记录条数
cat sent_news.json | grep -c "title"

# 手动触发清理（保留最近30天）
python -c "from storage import NewsStorage; s = NewsStorage(); s.cleanup_old_news(30)"
```

## 安全建议

1. **不要提交敏感配置到 Git**
   - `config.json` 已添加到 `.gitignore`
   - 使用环境变量管理密钥

2. **限制 API Key 权限**
   - Tavily API Key 只需要搜索权限
   - 飞书机器人只需要发消息权限

3. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **备份配置和数据**
   ```bash
   # 定期备份
   cp config.json config.backup.json
   cp sent_news.json sent_news.backup.json
   ```

## 故障排查

### 问题 1：推送到飞书失败

**现象：** 控制台显示 `❌ 推送失败`

**排查步骤：**
1. 检查 Webhook URL 是否正确
2. 在浏览器中测试网络连接
3. 查看飞书群设置，确认机器人未被移除
4. 运行 `python test_feishu.py` 单独测试

**解决方案：**
```bash
# 测试网络连接
curl -X POST "你的webhook_url" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"测试"}}'
```

### 问题 2：Tavily 搜索失败

**现象：** 控制台显示 `[Tavily] ❌ 搜索失败`

**排查步骤：**
1. 检查 API Key 是否正确
2. 检查 API 配额是否用尽
3. 检查网络连接

**解决方案：**
```bash
# 测试 API Key
curl -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"你的key","query":"test","max_results":1}'
```

### 问题 3：新闻重复推送

**现象：** 相同新闻被推送多次

**排查步骤：**
1. 检查 `sent_news.json` 是否存在
2. 检查文件写入权限
3. 查看日志确认是否成功记录

**解决方案：**
```bash
# 检查文件权限
ls -l sent_news.json

# 手动添加权限
chmod 666 sent_news.json

# 验证 JSON 格式
python -m json.tool sent_news.json
```

### 问题 4：Cron 任务不执行

**现象：** 到了时间但没有收到推送

**排查步骤：**
1. 检查 cron 服务是否运行：`systemctl status cron`
2. 查看 cron 日志：`grep CRON /var/log/syslog`
3. 确认路径是否正确
4. 测试 Python 环境：`which python3`

**解决方案：**
```bash
# 在 crontab 中使用绝对路径
0 8 * * * cd /绝对路径 && /usr/bin/python3 logistics_alert.py weather

# 测试 cron 命令（手动执行）
cd /你的路径 && /usr/bin/python3 logistics_alert.py weather
```

## 进阶功能

### 添加邮件推送

可以扩展 `feishu_sender.py`，添加邮件推送功能：

```python
import smtplib
from email.mime.text import MIMEText

def send_email(content: str, title: str):
    msg = MIMEText(content, 'html')
    msg['Subject'] = title
    msg['From'] = "your-email@example.com"
    msg['To'] = "recipient@example.com"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("your-email", "your-password")
        server.send_message(msg)
```

### 添加 Slack 推送

安装 `slack-sdk` 并添加：

```python
from slack_sdk import WebClient

slack_client = WebClient(token="xoxb-your-token")
slack_client.chat_postMessage(
    channel="#logistics",
    text=content
)
```

### 数据分析和报表

可以基于 `sent_news.json` 生成统计报表：

```python
import json
from collections import Counter

# 加载历史数据
with open("sent_news.json") as f:
    data = json.load(f)

# 统计最近30天的新闻数量
print(f"最近30天推送: {len(data['news'])} 条新闻")

# 分析高频关键词
# ... 进一步分析
```

## 系统架构图

```
┌─────────────────────────────────────────────────┐
│           定时任务调度器 (Cron/Schedule)          │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
    每天8:00          每天9:00
    天气检查          新闻检查
        │                 │
        ▼                 ▼
┌───────────────┐   ┌──────────────┐
│ Weather       │   │ News Monitor │
│ Monitor       │   │ + Storage    │
└───────┬───────┘   └──────┬───────┘
        │                  │
        │  ┌───────────────┤
        │  │               │
        ▼  ▼               ▼
    ┌─────────────┐   ┌─────────┐
    │   Tavily    │   │  去重    │
    │   Search    │   │  检查    │
    └──────┬──────┘   └────┬────┘
           │               │
           ▼               ▼
       ┌───────────────────────┐
       │   Feishu Sender       │
       │   (Webhook/Bot API)   │
       └───────────┬───────────┘
                   │
                   ▼
           ┌───────────────┐
           │  飞书群聊     │
           │  接收消息     │
           └───────────────┘
```

## 扩展建议

1. **多语言支持** - 添加中英文报告切换
2. **严重程度分级** - 根据关键词判断事件严重性
3. **地理位置过滤** - 精确到城市级别监控
4. **历史数据分析** - 生成月度/年度报表
5. **Web 管理界面** - 可视化配置和监控
6. **移动端推送** - 支持短信、企业微信等
7. **AI 摘要** - 使用 LLM 生成更智能的摘要

## 技术栈

- **Python 3.8+** - 主要编程语言
- **Tavily API** - 新闻和天气搜索
- **飞书 Open API** - 消息推送
- **schedule** - 定时任务调度
- **requests** - HTTP 请求
- **JSON** - 数据存储

## 文件说明

| 文件 | 用途 | 何时使用 |
|------|------|----------|
| `logistics_alert.py` | ⭐ 主程序（推荐） | 生产环境日常使用 |
| `demo_with_real_search.py` | 功能演示 | 测试和演示功能 |
| `test_feishu.py` | 飞书测试 | 验证飞书配置 |
| `main.py` | schedule版本 | 持续运行场景 |
| `run_daily_check.py` | 单次执行 | Cron 定时任务 |
| `main_with_mcp.py` | MCP版本 | Claude Code环境 |

## 获取帮助

- 查看演示：`python demo_with_real_search.py`
- 测试推送：`python test_feishu.py`
- 查看日志：`tail -f logs/*.log`
- 查看配置：`cat config.json`

## 版本历史

- **v1.0.0** (2026-02-19) - 初始版本
  - 天气预警每日推送
  - 物流新闻增量推送
  - 飞书 Webhook 集成
  - 自动去重机制

---

**祝使用愉快！**
