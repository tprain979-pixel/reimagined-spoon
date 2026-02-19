# 配置向导 - 10分钟完成配置

## 当前状态

✅ **已完成：**
- Python 依赖已安装（requests, schedule）
- 项目文件已创建
- 监控配置已设置

❌ **待完成：**
- 配置 Tavily API Key
- 配置飞书 Webhook

---

## 配置步骤

### 🔑 步骤 1：获取 Tavily API Key（3分钟）

#### 1.1 注册 Tavily 账号

1. **打开浏览器**，访问：<a href="https://tavily.com" target="_blank">https://tavily.com</a>

2. **点击 "Get Started"** 或 **"Sign Up"**

3. **选择注册方式**（推荐 Google）：
   ```
   🔵 Continue with Google  ← 推荐（最快）
   ⚫ Continue with GitHub
   📧 Email + Password
   ```

4. **完成授权**
   - 如果使用 Google：选择账号 → 允许授权
   - 如果使用邮箱：填写邮箱和密码 → 验证邮件

#### 1.2 获取 API Key

注册成功后会自动跳转到 **Dashboard**：

1. **找到 API Key**
   - Dashboard 首页会直接显示 "Your API Key"
   - 或左侧菜单 → "API Keys"

2. **复制 API Key**
   - 格式：`tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - 点击复制按钮 📋
   - 保存到安全的地方（不要分享！）

3. **查看配额**
   - 免费计划：每月 1,000 次搜索
   - 你的需求：每月约 60 次
   - 完全够用！✅

#### 1.3 填入配置文件

打开 `config.json`，找到这一行：

```json
"tavily_api_key": "YOUR_TAVILY_API_KEY",
```

替换为你的真实 API Key：

```json
"tavily_api_key": "tvly-abc123def456ghi789...",
```

**注意事项：**
- ⚠️ 保留双引号
- ⚠️ 不要有多余的空格
- ⚠️ 完整复制整个 API Key

#### 1.4 测试 API Key

运行测试脚本：

```bash
python test_tavily.py
```

**预期输出：**
```
✅ API Key 有效！
✅ 搜索成功，返回 X 条结果
```

---

### 📱 步骤 2：配置飞书 Webhook（3分钟）

#### 2.1 打开飞书群聊

1. **选择或创建群聊**
   - 可以使用现有群聊
   - 或创建新的专用群聊（推荐命名：物流预警）

2. **打开群设置**
   - 点击群名称
   - 或点击右上角 ⚙️ 图标

#### 2.2 添加自定义机器人

1. **进入机器人管理**
   - 群设置 → **群机器人**
   - 点击 **"添加机器人"**

2. **选择机器人类型**
   - 选择 **"自定义机器人"**
   - 不要选择其他预设机器人

3. **配置机器人**
   - 名称：`物流预警机器人`
   - 描述：`监控欧洲物流天气和新闻`
   - 图标：可选择默认或上传自定义图标

4. **安全设置**（可选）
   - 签名校验：一般不需要（留空即可）
   - IP 白名单：一般不需要

5. **完成添加**
   - 点击 **"添加"** 或 **"确定"**
   - 系统会生成 Webhook URL

#### 2.3 复制 Webhook URL

**重要：** 机器人添加成功后会显示 Webhook URL

1. **复制 URL**
   ```
   格式：https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

2. **点击复制按钮** 📋

3. **保存 URL**（不要关闭弹窗，先完成配置）

#### 2.4 填入配置文件

打开 `config.json`，找到这一行：

```json
"webhook_url": "YOUR_FEISHU_WEBHOOK_URL",
```

替换为你的 Webhook URL：

```json
"webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的token",
```

**注意事项：**
- ⚠️ 保留双引号
- ⚠️ 完整复制整个 URL
- ⚠️ 不要有换行或空格

#### 2.5 测试飞书推送

运行测试脚本：

```bash
python test_feishu.py
```

**预期结果：**
1. 控制台显示：`✅ 测试成功！飞书推送功能正常工作`
2. 飞书群聊收到测试消息

**如果收不到消息：**
- 检查 Webhook URL 是否正确
- 确认机器人未被移除
- 查看群聊设置中机器人是否在线

---

### 🧪 步骤 3：运行完整测试（2分钟）

#### 3.1 检查配置

```bash
python check_config.py
```

**预期输出：**
```
✅ 通过: 6 项
❌ 失败: 0 项

🎉 所有配置检查通过！
```

#### 3.2 运行功能演示

```bash
# 预览模式（不推送）
python demo_with_real_search.py

# 推送模式（会发送到飞书）
python demo_with_real_search.py --send
```

#### 3.3 执行真实检查

```bash
# 同时检查天气和新闻
python logistics_alert.py both

# 仅检查天气
python logistics_alert.py weather

# 仅检查新闻
python logistics_alert.py news
```

**预期结果：**
- 控制台显示搜索过程和结果
- 飞书群聊收到推送消息
- `sent_news.json` 记录新闻

---

### ⏰ 步骤 4：设置定时任务（2分钟）

#### Linux/Mac - 使用 Cron

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加以下行（修改为你的实际路径）
0 8 * * * cd /你的路径/logistics-alert-system && /usr/bin/python3 logistics_alert.py weather >> logs/weather.log 2>&1
0 9 * * * cd /你的路径/logistics-alert-system && /usr/bin/python3 logistics_alert.py news >> logs/news.log 2>&1

# 3. 保存并退出（:wq）

# 4. 查看已设置的任务
crontab -l
```

**时间说明：**
- `0 8 * * *` = 每天 8:00
- `0 9 * * *` = 每天 9:00
- 可以修改为任意时间

**创建日志目录：**
```bash
mkdir -p logs
```

#### Windows - 使用任务计划程序

1. **打开任务计划程序**
   - Win + R → 输入 `taskschd.msc`
   - 或搜索"任务计划程序"

2. **创建任务 - 天气预警**
   - 右键 → 创建基本任务
   - 名称：`物流天气预警`
   - 触发器：每天 → 8:00
   - 操作：启动程序
     - 程序：`C:\Python\python.exe`
     - 参数：`logistics_alert.py weather`
     - 起始于：`C:\你的路径\logistics-alert-system`

3. **创建任务 - 新闻监控**
   - 重复上述步骤
   - 名称：`物流新闻监控`
   - 时间：9:00
   - 参数：`logistics_alert.py news`

---

## 完整配置检查清单

使用此清单确保所有配置正确：

```
配置检查清单
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

环境准备
  ☐ Python 3.8+ 已安装
  ☐ pip 可以正常使用
  ☐ 运行 pip install -r requirements.txt

Tavily API 配置
  ☐ 访问 https://tavily.com 注册账号
  ☐ 在 Dashboard 获取 API Key
  ☐ 填入 config.json 的 tavily_api_key
  ☐ 运行 python test_tavily.py 测试

飞书配置
  ☐ 打开飞书群聊
  ☐ 添加自定义机器人
  ☐ 复制 Webhook URL
  ☐ 填入 config.json 的 webhook_url
  ☐ 运行 python test_feishu.py 测试

功能测试
  ☐ 运行 python check_config.py 检查配置
  ☐ 运行 python demo_with_real_search.py 查看演示
  ☐ 运行 python logistics_alert.py both 执行真实检查

定时任务
  ☐ 设置 cron 或任务计划程序
  ☐ 配置日志输出路径
  ☐ 测试定时任务是否执行

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 配置文件示例

完整的 `config.json` 应该是这样（填入真实值）：

```json
{
  "tavily_api_key": "tvly-abc123def456...",
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xyz-123-456..."
  },
  "monitoring": {
    "countries": ["Germany", "France", "Netherlands", "Belgium", "Poland"],
    "weather_keywords": [
      "extreme weather", "storm", "snow", "rain", "wind", "temperature"
    ],
    "news_keywords": [
      "strike", "fire", "warehouse", "port closure",
      "transport disruption", "logistics incident", "border closure"
    ],
    "weather_check_time": "08:00",
    "news_check_time": "09:00"
  },
  "storage": {
    "sent_news_file": "sent_news.json",
    "max_history_days": 30
  }
}
```

---

## 验证配置

运行自动检查脚本：

```bash
python check_config.py
```

**全部配置正确时显示：**
```
🎉 所有配置检查通过！

📋 下一步：
  1. 运行 'python test_tavily.py' 测试 API 连接
  2. 运行 'python test_feishu.py' 测试飞书推送
  3. 运行 'python logistics_alert.py both' 执行检查
  4. 设置 cron 定时任务
```

---

## 故障排除

### 问题：Tavily API 返回 401

**原因：** API Key 无效

**解决：**
1. 重新复制 API Key（确保完整）
2. 检查 config.json 中是否有多余字符
3. 在 Tavily Dashboard 重新生成 API Key

### 问题：飞书收不到消息

**原因：** Webhook 配置错误

**解决：**
1. 确认机器人未被移除（在群聊中查看）
2. 重新复制 Webhook URL
3. 尝试在浏览器中打开 URL 测试（会返回错误，但能验证 URL 格式）

### 问题：运行脚本报错 ModuleNotFoundError

**原因：** 依赖未安装

**解决：**
```bash
pip install -r requirements.txt
```

---

## 快速命令参考

```bash
# 安装依赖
pip install -r requirements.txt

# 检查配置
python check_config.py

# 测试 Tavily
python test_tavily.py

# 测试飞书
python test_feishu.py

# 查看演示
python demo_with_real_search.py

# 执行检查（推送到飞书）
python logistics_alert.py both

# 仅检查天气
python logistics_alert.py weather

# 仅检查新闻
python logistics_alert.py news
```

---

## 完成后的系统效果

### 每天早上 8:00 - 天气预警

飞书群聊会收到：

```
# 欧洲物流天气预警报告

**报告时间:** 2026-02-19 08:00:00
**监控区域:** 欧洲（重点：德国）

⚠️ **发现 2 条天气预警信息**

## 1. Storm warnings issued for northern Germany

Severe weather conditions expected...

**来源:** https://...

---

_提示: 请关注天气变化对物流运输的影响_
```

### 每天早上 9:00 - 物流新闻（仅新增时）

如果有新增事件，飞书群聊会收到：

```
# 欧洲物流突发事件预警

**报告时间:** 2026-02-19 09:00:00
**新增事件:** 2 条

🚨 **以下为新增物流相关事件，请注意关注**

## 1. Major strike at Hamburg port

**紧急程度:** 🔴 高

Workers at Hamburg port have initiated a strike...

**详情链接:** https://...

---

_系统已记录这些新闻，不会重复推送_
```

---

## 需要帮助？

**文档目录：**
- `SETUP_WIZARD.md` ← 你在这里（配置向导）
- `TAVILY_SETUP.md` - Tavily 详细注册指南
- `QUICKSTART.md` - 5分钟快速开始
- `USAGE_GUIDE.md` - 详细使用说明
- `README.md` - 项目介绍

**测试脚本：**
- `check_config.py` - 检查所有配置
- `test_tavily.py` - 测试 Tavily API
- `test_feishu.py` - 测试飞书推送
- `demo_with_real_search.py` - 功能演示

**有问题？**
- 查看上述文档
- 运行检查脚本诊断
- 查看日志文件：`logs/*.log`

---

**准备就绪？**

1. 先运行 `python check_config.py` 检查配置
2. 然后按照提示完成 Tavily 和飞书配置
3. 最后运行 `python logistics_alert.py both` 开始使用！

🎉 祝配置顺利！
