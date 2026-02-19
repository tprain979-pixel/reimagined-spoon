# 部署指南

## 部署方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Cron + Python** | 简单，无需额外服务 | 需要服务器持续运行 | 个人使用，轻量部署 |
| **Docker + Cron** | 隔离环境，易于迁移 | 需要 Docker 知识 | 生产环境，团队使用 |
| **云函数（AWS Lambda/阿里云FC）** | 无需维护服务器，按需付费 | 需要云平台配置 | 成本敏感，间歇运行 |
| **Kubernetes CronJob** | 高可用，自动重试 | 复杂度高 | 大规模企业应用 |

---

## 方案1：Linux Cron 部署（推荐入门）

### 环境要求
- Linux 服务器（Ubuntu/CentOS/Debian）
- Python 3.8+
- 稳定的网络连接

### 部署步骤

#### 1. 克隆或上传项目到服务器

```bash
# 上传到服务器
scp -r logistics-alert-system user@server:/opt/

# 或使用 git
git clone your-repo /opt/logistics-alert-system
```

#### 2. 安装依赖

```bash
cd /opt/logistics-alert-system
pip3 install -r requirements.txt
```

#### 3. 配置文件

```bash
# 复制配置模板
cp config.json config.json.backup

# 编辑配置文件
vim config.json
```

填入：
- `tavily_api_key`: Tavily API 密钥
- `feishu.webhook_url`: 飞书 Webhook 地址

#### 4. 测试运行

```bash
# 测试飞书推送
python test_feishu.py

# 测试完整检查
python logistics_alert.py both
```

#### 5. 配置 Cron

```bash
# 创建日志目录
mkdir -p logs

# 编辑 crontab
crontab -e

# 添加定时任务（修改路径）
0 8 * * * cd /opt/logistics-alert-system && python3 logistics_alert.py weather >> logs/weather.log 2>&1
0 9 * * * cd /opt/logistics-alert-system && python3 logistics_alert.py news >> logs/news.log 2>&1
```

#### 6. 验证 Cron

```bash
# 查看 cron 日志
grep CRON /var/log/syslog

# 查看应用日志
tail -f /opt/logistics-alert-system/logs/*.log
```

---

## 方案2：Docker 部署

### 部署步骤

#### 1. 构建镜像

```bash
docker build -t logistics-alert:latest .
```

#### 2. 创建 .env 文件

```bash
cp .env.example .env
# 编辑 .env，填入 TAVILY_API_KEY
```

#### 3. 运行容器（手动触发）

```bash
docker run --rm \
  --env-file .env \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/sent_news.json:/app/sent_news.json \
  -v $(pwd)/logs:/app/logs \
  logistics-alert:latest
```

#### 4. 配合 Cron 使用（推荐）

在宿主机上配置 cron 定时启动容器：

```bash
# 编辑 crontab
crontab -e

# 添加定时任务
0 8 * * * docker run --rm --env-file /opt/logistics-alert/.env -v /opt/logistics-alert/config.json:/app/config.json -v /opt/logistics-alert/sent_news.json:/app/sent_news.json logistics-alert:latest weather
0 9 * * * docker run --rm --env-file /opt/logistics-alert/.env -v /opt/logistics-alert/config.json:/app/config.json -v /opt/logistics-alert/sent_news.json:/app/sent_news.json logistics-alert:latest news
```

---

## 方案3：云函数部署

### AWS Lambda

#### 1. 准备部署包

```bash
# 安装依赖到 package 目录
pip install -r requirements.txt -t package/

# 复制代码文件
cp *.py package/
cp config.json package/

# 打包
cd package && zip -r ../lambda_function.zip . && cd ..
```

#### 2. 创建 Lambda 函数

- 运行时：Python 3.11
- 处理程序：`logistics_alert.main`
- 超时：5 分钟
- 环境变量：`TAVILY_API_KEY`

#### 3. 配置 EventBridge 定时触发

- 创建规则，Cron 表达式：
  - 天气：`cron(0 8 * * ? *)`（每天8:00 UTC）
  - 新闻：`cron(0 9 * * ? *)`（每天9:00 UTC）

### 阿里云函数计算

类似步骤，使用阿里云函数计算 + 定时触发器。

---

## 方案4：Kubernetes CronJob

### 1. 创建 ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logistics-alert-config
data:
  config.json: |
    {
      "tavily_api_key": "从 Secret 读取",
      "feishu": {
        "webhook_url": "从 Secret 读取"
      },
      ...
    }
```

### 2. 创建 Secret

```bash
kubectl create secret generic logistics-alert-secrets \
  --from-literal=tavily-api-key=tvly-xxxxx \
  --from-literal=feishu-webhook=https://open.feishu.cn/...
```

### 3. 创建 CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: logistics-weather-alert
spec:
  schedule: "0 8 * * *"  # 每天 8:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: alert
            image: logistics-alert:latest
            command: ["python", "logistics_alert.py", "weather"]
            envFrom:
            - secretRef:
                name: logistics-alert-secrets
            volumeMounts:
            - name: config
              mountPath: /app/config.json
              subPath: config.json
          volumes:
          - name: config
            configMap:
              name: logistics-alert-config
          restartPolicy: OnFailure
```

---

## 监控和维护

### 日志管理

#### 查看日志
```bash
# Cron 部署
tail -f logs/weather.log
tail -f logs/news.log

# Docker 部署
docker logs logistics-alert-system

# Kubernetes 部署
kubectl logs -f job/logistics-weather-alert-xxxxx
```

#### 日志清理

```bash
# 自动清理 30 天前的日志（添加到 crontab）
0 2 * * 0 find /opt/logistics-alert-system/logs -name "*.log" -mtime +30 -delete
```

### 健康检查

创建健康检查脚本 `health_check.sh`：

```bash
#!/bin/bash
LOG_DIR="/opt/logistics-alert-system/logs"
TODAY=$(date +%Y%m%d)

# 检查今天是否有日志生成
if [ ! -f "$LOG_DIR/weather_$TODAY.log" ]; then
    echo "警告：今日天气检查未执行"
    # 发送告警到飞书或邮件
fi

if [ ! -f "$LOG_DIR/news_$TODAY.log" ]; then
    echo "警告：今日新闻检查未执行"
    # 发送告警到飞书或邮件
fi
```

配置每日健康检查：
```bash
0 12 * * * /opt/logistics-alert-system/health_check.sh
```

### 数据备份

```bash
# 备份配置和新闻记录
#!/bin/bash
BACKUP_DIR="/backup/logistics-alert"
mkdir -p $BACKUP_DIR

cp config.json $BACKUP_DIR/config_$(date +%Y%m%d).json
cp sent_news.json $BACKUP_DIR/sent_news_$(date +%Y%m%d).json

# 只保留最近 7 天的备份
find $BACKUP_DIR -name "*.json" -mtime +7 -delete
```

添加到 crontab：
```bash
0 0 * * * /opt/logistics-alert-system/backup.sh
```

---

## 故障排查

### 问题1：推送失败

**症状：** 日志显示 "推送失败"

**排查步骤：**
1. 检查飞书 Webhook URL 是否正确
2. 测试网络连接：`curl -I https://open.feishu.cn`
3. 验证 Webhook：`curl -X POST 你的webhook -H 'Content-Type: application/json' -d '{"msg_type":"text","content":{"text":"test"}}'`
4. 检查飞书机器人是否被移除

### 问题2：没有搜索结果

**症状：** 日志显示 "找到 0 条结果"

**排查步骤：**
1. 检查 Tavily API Key 是否正确
2. 验证 API 配额：访问 Tavily 控制台查看剩余额度
3. 调整搜索关键词，使其更加宽泛
4. 手动测试 Tavily 搜索：
   ```bash
   curl -X POST https://api.tavily.com/search \
     -H 'Content-Type: application/json' \
     -d '{"api_key":"你的key","query":"Germany logistics weather","max_results":5}'
   ```

### 问题3：重复推送新闻

**症状：** 相同新闻被多次推送

**排查步骤：**
1. 检查 `sent_news.json` 文件权限
2. 确认文件没有被其他进程占用
3. 查看日志确认是否有"已记录新闻"的输出
4. 检查是否有多个 cron 任务同时运行

### 问题4：定时任务未执行

**症状：** 到了指定时间但没有推送

**排查步骤：**
1. 检查 cron 服务是否运行：`systemctl status cron`
2. 查看 cron 日志：`grep CRON /var/log/syslog`
3. 验证 crontab 语法：使用 <a href="https://crontab.guru" target="_blank">https://crontab.guru</a>
4. 确认脚本有执行权限：`chmod +x logistics_alert.py`
5. 使用绝对路径：`/usr/bin/python3 /opt/logistics-alert-system/logistics_alert.py`

---

## 性能优化

### 1. 减少 API 调用

```json
// config.json
{
  "monitoring": {
    "weather_check_interval": "12h",  // 每12小时检查一次天气
    "news_check_interval": "6h"       // 每6小时检查一次新闻
  }
}
```

### 2. 限流保护

添加重试和延迟机制，避免 API 限流。

### 3. 缓存优化

对于天气数据，可以添加短时缓存（如 1 小时）。

---

## 安全建议

1. **保护敏感信息**
   - 不要将 `config.json` 提交到 Git
   - 使用 `.env` 文件或环境变量存储密钥
   - 在 `.gitignore` 中添加：
     ```
     config.json
     .env
     sent_news.json
     logs/
     ```

2. **API Key 管理**
   - 定期轮换 API Key
   - 使用密钥管理服务（AWS Secrets Manager, HashiCorp Vault）

3. **访问控制**
   - 限制文件权限：`chmod 600 config.json`
   - 使用专用用户运行服务

4. **网络安全**
   - 使用 HTTPS
   - 配置防火墙规则

---

## 扩展开发

### 添加新的监控关键词

编辑 `config.json`：

```json
{
  "monitoring": {
    "news_keywords": [
      "strike",
      "fire",
      "warehouse",
      "port closure",
      "transport disruption",
      "logistics incident",
      "border closure",
      "customs delay",      // 新增：海关延误
      "highway closure",    // 新增：高速公路封闭
      "fuel shortage"       // 新增：燃料短缺
    ]
  }
}
```

### 添加更多推送渠道

参考 `feishu_sender.py`，创建新的推送模块：

```python
# email_sender.py
class EmailSender:
    def send_message(self, content: str, title: str):
        # 实现邮件推送逻辑
        pass

# telegram_sender.py
class TelegramSender:
    def send_message(self, content: str, title: str):
        # 实现 Telegram 推送逻辑
        pass
```

### 添加 Web 管理界面

使用 Flask/FastAPI 创建简单的 Web 界面：
- 查看推送历史
- 手动触发检查
- 修改配置参数
- 查看系统状态

---

## 生产环境检查清单

部署到生产环境前，请确认：

- [ ] 已完成功能测试
- [ ] 配置文件中没有测试数据
- [ ] API Key 配额充足
- [ ] 飞书 Webhook 或机器人配置正确
- [ ] 定时任务时区设置正确
- [ ] 日志目录已创建且有写入权限
- [ ] 配置了日志清理机制
- [ ] 配置了健康检查和告警
- [ ] 备份了配置文件
- [ ] 文档已更新
- [ ] 团队成员已培训

---

## 维护计划

### 每日
- 查看推送是否正常
- 检查是否有异常日志

### 每周
- 审查推送内容质量
- 调整搜索关键词（如有需要）
- 清理旧日志

### 每月
- 检查 API 用量和成本
- 更新依赖包版本
- 备份历史数据

### 每季度
- 评估监控效果
- 优化搜索策略
- 更新文档

---

## 技术支持

如遇到问题，请：
1. 查看日志文件
2. 参考"故障排查"章节
3. 联系系统管理员

---

## 版本历史

- **v1.0.0** (2026-02-19)
  - 初始版本
  - 支持天气预警每日推送
  - 支持物流新闻增量推送
  - 集成飞书推送
