# Cron 定时任务设置指南

## ✅ 系统已完全配置并测试成功

### 已完成的配置

1. ✅ **Tavily API** - 已配置，配额充足（996/1,000）
2. ✅ **飞书 Webhook** - 已配置并测试成功
3. ✅ **中英文双语** - 推送内容已优化为中英文双语格式
4. ✅ **排版优化** - 消息格式美观，结构清晰
5. ✅ **真实测试** - 天气和新闻推送成功

### 你的飞书群现在应该收到了

刚才测试发送的**中英文双语消息**：
1. 🌤️ 欧洲物流天气预警（含 10 条真实天气信息）
2. 🚨 欧洲物流突发事件预警（含 15 条真实物流新闻）

**消息特点：**
- 📝 标题和内容都有中英文
- 🎨 使用图标增强可读性
- 📊 紧急程度分级（高/中/低）
- 🔗 包含详情链接
- 📋 排版清晰，层次分明

---

## ⏰ Cron 定时任务设置

由于当前环境限制，需要你在**本地服务器或生产环境**中手动设置 cron。

### 方案 1：推荐模式（每天 2 次）⭐

**配额消耗：** 120 次/月（12%）
**执行时间：** 早上 8:00, 9:00 + 晚上 18:00, 19:00

#### 设置步骤

在你的服务器上执行：

```bash
# 1. 切换到项目目录
cd /app/workspace/7415868573489743386/1/2/157

# 2. 创建日志目录
mkdir -p logs

# 3. 编辑 crontab
crontab -e

# 4. 复制以下内容到编辑器中
```

**复制这些配置：**

```cron
# 欧洲物流预警系统 - 每天 2 次（推荐）
# 早上检查
0 8 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
0 9 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1

# 晚上检查
0 18 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
0 19 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
```

```bash
# 5. 保存退出
# - Vi/Vim: 按 ESC，输入 :wq，回车
# - Nano: 按 Ctrl+X，按 Y，回车

# 6. 验证设置
crontab -l
```

---

### 方案 2：节省模式（每天 1 次）

**配额消耗：** 60 次/月（6%）
**执行时间：** 早上 8:00, 9:00

```cron
# 欧洲物流预警系统 - 每天 1 次（节省）
0 8 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
0 9 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
```

---

### 方案 3：高频模式（每天 4 次）

**配额消耗：** 240 次/月（24%）
**执行时间：** 6:00, 12:00, 18:00, 22:00

```cron
# 欧洲物流预警系统 - 每天 4 次（高频）
0 6 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
30 6 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
0 12 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
30 12 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
0 18 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
30 18 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
0 22 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py weather >> /app/workspace/7415868573489743386/1/2/157/logs/weather.log 2>&1
30 22 * * * cd /app/workspace/7415868573489743386/1/2/157 && /usr/bin/python3 logistics_alert_full.py news >> /app/workspace/7415868573489743386/1/2/157/logs/news.log 2>&1
```

---

## 📋 Cron 时间格式说明

```
分钟 小时 日期 月份 星期 命令
│   │   │   │   │
│   │   │   │   └─── 0-6 (0=周日)
│   │   │   └────── 1-12
│   │   └─────────── 1-31
│   └───────────────── 0-23
└───────────────────── 0-59

示例：
0 8 * * *    → 每天 8:00
0 */6 * * *  → 每 6 小时一次
30 9 * * 1   → 每周一 9:30
```

---

## 🛠️ 快速设置命令

### 一键设置（推荐模式）

```bash
# 在你的服务器上执行
cd /app/workspace/7415868573489743386/1/2/157

# 备份现有 crontab
crontab -l > crontab_backup.txt 2>/dev/null || true

# 添加定时任务
(crontab -l 2>/dev/null; echo ""; cat cron_config.txt) | crontab -

# 验证设置
crontab -l
```

### 验证定时任务

```bash
# 查看已设置的任务
crontab -l | grep logistics

# 应该显示 4 行任务配置
```

---

## 📱 中英文双语推送效果预览

### 天气预警消息示例

```
# 🌤️ 欧洲物流天气预警 | Europe Logistics Weather Alert

📅 报告时间 | Report Time: 2026-02-19 08:00:00
📍 监控区域 | Monitoring Area: 欧洲重点国家（德国、法国、荷兰、比利时、波兰）
🔍 数据来源 | Data Source: Tavily Real-time Search

---

## ⚠️ 天气预警汇总 | Weather Alert Summary

🔔 预警数量 | Alert Count: 10 条 | 10 alerts

---

### 1. Storm warnings issued for northern Germany

📄 详情 | Details:

Severe weather conditions expected with high winds and heavy
rainfall. Transport authorities warn of potential delays...

🔗 来源链接 | Source: https://...

---

💡 温馨提示 | Tips:
- 🚚 请关注天气变化对物流运输的影响
- 🚛 Please monitor weather impacts on logistics operations
- 📞 如有紧急情况请及时调整运输计划
- 📱 Adjust transport plans promptly if necessary
```

### 物流新闻消息示例

```
# 🚨 欧洲物流突发事件预警 | Europe Logistics Incident Alert

📅 报告时间 | Report Time: 2026-02-19 09:00:00
📊 新增事件 | New Incidents: 15 条 | 15 alerts
📍 监控区域 | Monitoring Area: 德国、法国、荷兰、比利时、波兰
🔍 数据来源 | Data Source: Tavily Real-time Search (Past 24 hours)

---

## ⚠️ 新增事件详情 | New Incident Details

⚡ 中文：以下为过去24小时内新增的物流相关事件，请注意关注
⚡ English: Following incidents occurred in the past 24 hours

---

### 📰 1. Major Strike at Hamburg Port

⚡ 紧急程度 | Urgency: 🔴 高 | 🔴 High

📋 事件描述 | Description:

Workers at Hamburg port have initiated a strike demanding
better wages. The strike affects major shipping operations...

🔗 详情链接 | Source: https://...

---

💡 重要提示 | Important Notes:

✅ 中文：系统已记录这些事件，相同事件不会重复推送

✅ English: These incidents have been recorded and will not be pushed repeatedly

📞 中文：如遇影响请及时调整物流计划或联系相关部门

📱 English: Please adjust logistics plans or contact relevant departments if affected
```

---

## 🎯 推送消息优化特点

### 排版优化

1. **清晰的层次结构**
   - 使用标题层级（#, ##, ###）
   - 分隔线区分不同部分
   - 合理的空行间距

2. **图标增强可读性**
   - 🌤️ 天气预警
   - 🚨 突发事件
   - 📅 时间信息
   - 📍 区域信息
   - ⚡ 紧急程度
   - 🔗 链接

3. **紧急程度分级**
   - 🔴 高（High）：相关性 > 0.8
   - 🟡 中（Medium）：相关性 > 0.5
   - 🟢 低（Low）：相关性 ≤ 0.5

### 中英文双语

1. **标题双语**
   - 中文 | English 格式
   - 便于国际团队使用

2. **关键信息双语**
   - 时间、区域、数量
   - 紧急程度、提示信息

3. **内容保持原文**
   - 搜索结果的标题和内容保持原文（通常是英文）
   - 避免机器翻译错误

---

## 🔍 验证定时任务

### 查看已设置的任务

```bash
# 列出所有 cron 任务
crontab -l

# 仅查看物流预警相关任务
crontab -l | grep logistics
```

### 测试定时任务

```bash
# 手动执行一次（测试是否正常）
cd /app/workspace/7415868573489743386/1/2/157
python3 logistics_alert_full.py both

# 查看日志输出
tail -f logs/weather.log
tail -f logs/news.log
```

### 查看日志文件

```bash
# 查看天气日志（最近 20 行）
tail -20 logs/weather.log

# 查看新闻日志（最近 20 行）
tail -20 logs/news.log

# 实时监控日志
tail -f logs/*.log

# 查看特定日期的日志
grep "2026-02-19" logs/*.log
```

---

## 📊 定时任务方案对比

| 方案 | 执行时间 | 每日次数 | 每月消耗 | 配额占用 | 适用场景 |
|------|----------|----------|----------|----------|----------|
| **节省模式** | 08:00, 09:00 | 2次 | 60次 | 6% | 低频需求 |
| **推荐模式⭐** | 08:00, 09:00, 18:00, 19:00 | 4次 | 120次 | 12% | 日常监控 |
| **高频模式** | 每6小时 | 8次 | 240次 | 24% | 重要时期 |
| **极高频** | 每4小时 | 12次 | 360次 | 36% | 紧急响应 |

### 推荐理由

**推荐模式（每天 2 次）** 最适合你：
- ✅ 早晚各一次，覆盖全天
- ✅ 配额仅用 12%，非常充裕
- ✅ 及时性好，不会漏掉重要事件
- ✅ 剩余 880 次配额可应急使用

---

## 🚀 手动执行命令

如果需要立即检查，无需等待定时任务：

```bash
# 切换到项目目录
cd /app/workspace/7415868573489743386/1/2/157

# 完整检查（天气 + 新闻）
python3 logistics_alert_full.py both

# 仅检查天气
python3 logistics_alert_full.py weather

# 仅检查新闻
python3 logistics_alert_full.py news
```

---

## 📝 Cron 配置文件位置

我已经为你生成了配置文件：
- **cron_config.txt** - 推荐模式配置（可直接复制）
- **crontab.example** - 其他配置示例

---

## 🔧 故障排查

### 问题 1：定时任务不执行

**检查步骤：**

```bash
# 1. 确认 cron 服务运行
systemctl status cron      # Ubuntu/Debian
systemctl status crond     # CentOS/RHEL

# 2. 查看 cron 日志
grep CRON /var/log/syslog  # Ubuntu/Debian
tail -f /var/log/cron      # CentOS/RHEL

# 3. 测试命令能否手动执行
cd /app/workspace/7415868573489743386/1/2/157 && python3 logistics_alert_full.py weather

# 4. 检查 Python 路径
which python3
```

### 问题 2：没有收到飞书消息

**检查步骤：**

```bash
# 1. 查看日志文件
cat logs/weather.log
cat logs/news.log

# 2. 手动测试推送
python3 test_feishu.py

# 3. 检查配置文件
cat config.json | grep webhook_url
```

### 问题 3：路径错误

**解决方案：**

如果你的项目不在 `/app/workspace/7415868573489743386/1/2/157`，需要修改 cron 配置中的路径。

使用相对路径版本：

```bash
# 获取当前绝对路径
pwd

# 假设输出：/home/user/logistics-alert-system
# 则修改 cron 配置中的路径为该路径
```

---

## 📈 监控和维护

### 每日检查（自动）

系统会自动执行，你只需：
1. 📱 在飞书查看推送消息
2. 📊 关注天气预警
3. 🚨 注意物流突发事件

### 每周检查（手动）

```bash
# 1. 查看日志确认正常运行
tail -50 logs/weather.log
tail -50 logs/news.log

# 2. 查看新闻记录数量
grep -c '"title"' sent_news.json

# 3. 检查 Tavily 配额使用
# 访问 https://app.tavily.com
```

### 每月维护

```bash
# 1. 清理旧日志（保留最近 30 天）
find logs/ -name "*.log" -mtime +30 -delete

# 2. 检查配额使用情况
# 登录 Tavily Dashboard 查看

# 3. 评估监控效果
# 根据实际需求调整关键词和国家范围
```

---

## 🎊 完成！

### 当前状态

```
系统配置：████████████████████ 100% 完成

✅ Tavily API：已配置，配额充足（996/1,000）
✅ 飞书 Webhook：已配置，推送成功
✅ 中英文双语：已实现，格式美观
✅ 功能测试：天气和新闻推送成功
✅ 去重功能：已验证有效
✅ Cron 配置：已生成，待部署
```

### 最后一步

**在你的生产服务器上：**

1. 复制项目文件到服务器
2. 运行 `crontab -e`
3. 粘贴 `cron_config.txt` 中的配置
4. 保存退出

**完成后：**
- ⏰ 系统将自动每日推送
- 📱 你在飞书接收通知
- 🚀 无需人工干预

---

## 📞 快速命令参考

```bash
# 设置定时任务
crontab -e

# 查看定时任务
crontab -l

# 移除定时任务
crontab -r

# 手动执行检查
python3 logistics_alert_full.py both

# 查看日志
tail -f logs/*.log

# 查看配额使用
cat sent_news.json | grep -c title
```

---

## 🎉 恭喜！

系统已完全配置成功：
- ✅ 中英文双语推送
- ✅ 排版清晰美观
- ✅ 功能测试通过
- ✅ Cron 配置已生成

**查看你的飞书群，应该已经收到了精美的中英文双语推送消息！**

下一步只需在生产服务器上设置 cron，系统就会自动运行。🚀
