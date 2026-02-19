# 快速开始指南

## 5分钟快速配置

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2：获取 Tavily API Key

1. 访问 <a href="https://tavily.com" target="_blank">https://tavily.com</a>
2. 注册账号并获取 API Key
3. 记录你的 API Key（格式：`tvly-xxxxxxxx`）

### 步骤 3：配置飞书 Webhook

1. 在飞书群聊中添加自定义机器人：
   - 点击群设置 ⚙️
   - 选择 "群机器人"
   - 点击 "添加机器人"
   - 选择 "自定义机器人"
   - 设置名称：`物流预警机器人`
   - 复制生成的 Webhook URL

2. 编辑 `config.json`，填入 Webhook URL：
   ```json
   {
     "tavily_api_key": "tvly-你的API密钥",
     "feishu": {
       "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/你的token"
     }
   }
   ```

### 步骤 4：测试推送

```bash
python test_feishu.py
```

如果看到飞书群聊收到测试消息，说明配置成功！

### 步骤 5：执行首次检查

```bash
# 完整检查（天气 + 新闻）
python logistics_alert.py both

# 或分别检查
python logistics_alert.py weather
python logistics_alert.py news
```

### 步骤 6：设置定时任务

#### 方式A：使用 Cron（Linux/Mac）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（修改路径）
0 8 * * * cd /你的路径/logistics-alert-system && python logistics_alert.py weather
0 9 * * * cd /你的路径/logistics-alert-system && python logistics_alert.py news
```

#### 方式B：使用 Windows 任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每天，设置时间
4. 操作：启动程序
   - 程序：`python.exe`
   - 参数：`logistics_alert.py weather`
   - 起始于：项目目录路径

#### 方式C：使用 Docker（推荐生产环境）

```bash
# 构建镜像
docker build -t logistics-alert .

# 手动运行
docker run --rm \
  -e TAVILY_API_KEY=你的key \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/sent_news.json:/app/sent_news.json \
  logistics-alert

# 配合 cron 使用
0 8 * * * docker run --rm -e TAVILY_API_KEY=你的key -v /路径/config.json:/app/config.json logistics-alert weather
```

## 完成！

现在系统会：
- 每天早上 8:00 推送天气预警（无论是否有预警）
- 每天早上 9:00 检查物流新闻，有新增时推送

## 常见问题

**Q: 如何修改监控的国家？**

A: 编辑 `config.json` 中的 `monitoring.countries` 数组。

**Q: 如何调整搜索关键词？**

A: 编辑 `config.json` 中的 `monitoring.weather_keywords` 和 `monitoring.news_keywords`。

**Q: 如何避免重复推送？**

A: 系统已自动处理。新闻推送会记录到 `sent_news.json`，相同新闻不会重复推送。

**Q: Tavily API 有免费额度吗？**

A: 是的，Tavily 提供免费试用额度。具体请查看官网定价。

**Q: 可以推送到多个飞书群吗？**

A: 当前版本支持一个群。如需多群推送，可以配置多个 webhook_url 并修改代码。

## 下一步

- 查看 `README.md` 了解详细文档
- 根据实际需求调整监控参数
- 配置日志记录和监控告警
