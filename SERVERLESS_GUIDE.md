# 无服务器部署指南 - 3种方案

## 不想使用服务器？有 3 种方案！

### 方案对比

| 方案 | 优点 | 缺点 | 推荐度 | 成本 |
|------|------|------|--------|------|
| **GitHub Actions** | 完全免费，无需服务器，自动运行 | 需要 GitHub 账号 | ⭐⭐⭐⭐⭐ | 免费 |
| **本地电脑运行** | 配置简单，立即可用 | 需要电脑开机 | ⭐⭐⭐ | 免费 |
| **云函数服务** | 稳定可靠，无需维护 | 需要云服务账号 | ⭐⭐⭐⭐ | 低成本 |

---

## 方案 1：GitHub Actions（最推荐）⭐

### 优势
- ✅ **完全免费** - GitHub Actions 对公开仓库免费
- ✅ **无需服务器** - GitHub 自动执行
- ✅ **自动运行** - 设置后无需管理
- ✅ **稳定可靠** - GitHub 基础设施保障
- ✅ **日志完整** - 自动保存执行日志

### 配置步骤（10 分钟）

#### 步骤 1：创建 GitHub 仓库

1. 访问 <a href="https://github.com" target="_blank">https://github.com</a>
2. 点击右上角 "+" → "New repository"
3. 仓库名称：`logistics-alert-system`
4. 选择 **Private**（私有仓库，保护配置安全）
5. 点击 "Create repository"

#### 步骤 2：上传项目代码

```bash
# 在项目目录中执行
cd /app/workspace/7415868573489743386/1/2/157

# 初始化 Git
git init

# 添加文件
git add .

# 提交
git commit -m "初始化欧洲物流预警系统"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/logistics-alert-system.git

# 推送
git push -u origin main
```

#### 步骤 3：配置 GitHub Secrets

1. 打开你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**

**添加以下 2 个 secrets：**

**Secret 1: TAVILY_API_KEY**
- Name: `TAVILY_API_KEY`
- Value: `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`

**Secret 2: FEISHU_WEBHOOK_URL**
- Name: `FEISHU_WEBHOOK_URL`
- Value: `https://open.feishu.cn/open-apis/bot/v2/hook/a14fed8b-a114-429a-8c14-c54db1666c97`

#### 步骤 4：启用 GitHub Actions

1. 在仓库中点击 **Actions** 标签
2. 如果提示启用 Actions，点击 **"I understand my workflows, go ahead and enable them"**
3. 查看工作流：**"欧洲物流预警推送"**

#### 步骤 5：手动测试

1. 在 Actions 页面，点击左侧的 **"欧洲物流预警推送"**
2. 点击右上角 **"Run workflow"**
3. 选择 `both` → 点击 **"Run workflow"**
4. 等待执行完成（约 30 秒）
5. 查看飞书群是否收到消息

#### 步骤 6：自动运行

设置完成后，GitHub Actions 会自动：
- ⏰ 每天早上 8:00（北京时间）执行天气和新闻检查
- ⏰ 每天晚上 18:00（北京时间）执行天气和新闻检查
- 📱 自动推送到飞书

### 时区说明

GitHub Actions 使用 **UTC 时间**，需要转换：

```
北京时间 08:00 = UTC 00:00 ✅ 已配置
北京时间 18:00 = UTC 10:00 ✅ 已配置
```

### 配置文件位置

- `.github/workflows/daily_check.yml` - GitHub Actions 配置文件

### 查看执行日志

1. 打开仓库 → **Actions** 标签
2. 点击任意执行记录
3. 查看详细日志和输出

### 优点总结

- ✅ 无需服务器，完全免费
- ✅ 无需保持电脑开机
- ✅ 自动执行，无需人工干预
- ✅ 日志完整，便于排查
- ✅ 私有仓库，配置安全

---

## 方案 2：本地电脑持续运行

### 优势
- ✅ **配置最简单** - 一条命令启动
- ✅ **立即可用** - 无需额外配置
- ✅ **完全免费** - 不需要任何服务

### 劣势
- ⚠️ **需要开机** - 电脑关机或休眠会停止
- ⚠️ **需要保持程序运行** - 窗口关闭会停止

### 使用步骤（1 分钟）

#### 步骤 1：启动程序

```bash
# Windows
python run_local.py

# Mac/Linux
python3 run_local.py

# 或后台运行（Linux/Mac）
nohup python3 run_local.py > logs/run.log 2>&1 &
```

#### 步骤 2：查看输出

```
======================================================================
        欧洲物流预警推送系统 - 本地运行版本
======================================================================

⏰ 启动时间: 2026-02-19 12:30:00

📋 定时计划:
  - 天气预警: 每天 08:00 和 18:00
  - 物流新闻: 每天 09:00 和 19:00

💡 提示:
  - 保持此窗口运行即可实现定时推送
  - 按 Ctrl+C 可停止程序
  - 关闭窗口后程序会停止

======================================================================

✅ 定时任务已设置

⏳ 等待下次执行...

⏰ 下次执行: 2026-02-19 18:00:00
```

#### 步骤 3：保持运行

**Windows：**
- 保持命令行窗口打开
- 或使用任务计划程序开机自动启动

**Mac/Linux：**
- 使用 `nohup` 后台运行
- 或设置为系统服务（systemd）

### 后台运行（Linux/Mac）

```bash
# 后台运行
nohup python3 run_local.py > logs/run.log 2>&1 &

# 查看进程
ps aux | grep run_local

# 停止程序
pkill -f run_local.py

# 查看日志
tail -f logs/run.log
```

### Windows 开机自动启动

1. 创建批处理文件 `start_logistics_alert.bat`：

```batch
@echo off
cd /d "C:\你的路径\logistics-alert-system"
python run_local.py
pause
```

2. 将批处理文件快捷方式放到启动文件夹：
   - Win + R → `shell:startup`
   - 粘贴快捷方式

---

## 方案 3：云函数服务

### 优势
- ✅ **稳定可靠** - 云厂商保障
- ✅ **无需维护** - 无需管理服务器
- ✅ **按量计费** - 使用量极低，成本几乎为 0

### 支持的云服务

#### 阿里云函数计算（推荐）

**费用：** 每月前 100 万次调用免费

**配置步骤：**

1. 访问 <a href="https://fc.console.aliyun.com" target="_blank">https://fc.console.aliyun.com</a>
2. 创建函数
   - 运行时：Python 3.10
   - 上传代码：打包项目为 zip
3. 配置环境变量：
   - `TAVILY_API_KEY`
   - `FEISHU_WEBHOOK_URL`
4. 设置触发器：
   - 类型：定时触发
   - 时间：`0 8,18 * * *`（每天 8:00 和 18:00）
5. 保存并测试

**月度费用估算：**
- 调用次数：120 次/月
- 免费额度：100 万次/月
- **费用：0 元**

#### AWS Lambda

**费用：** 每月前 100 万次请求免费

**配置步骤：**

1. 访问 <a href="https://console.aws.amazon.com/lambda" target="_blank">https://console.aws.amazon.com/lambda</a>
2. 创建函数
   - 运行时：Python 3.11
   - 上传代码
3. 配置环境变量
4. 设置 EventBridge 触发器：
   - Schedule expression: `cron(0 0,10 * * ? *)`

#### 腾讯云函数

**费用：** 每月有免费额度

**配置步骤：**

1. 访问 <a href="https://console.cloud.tencent.com/scf" target="_blank">https://console.cloud.tencent.com/scf</a>
2. 创建函数
3. 配置触发器：定时触发
4. 设置环境变量

---

## 🎯 推荐方案选择

### 根据你的情况选择

#### 推荐：GitHub Actions ⭐⭐⭐⭐⭐

**适合你，如果：**
- ✅ 有 GitHub 账号（或愿意注册）
- ✅ 不想管理服务器
- ✅ 希望完全免费
- ✅ 需要稳定自动运行

**配置难度：** ⭐⭐（10 分钟）
**费用：** 免费
**稳定性：** ⭐⭐⭐⭐⭐

#### 备选：本地电脑运行 ⭐⭐⭐

**适合你，如果：**
- ✅ 电脑经常开机
- ✅ 想立即使用，不想配置 GitHub
- ✅ 不介意电脑关机时暂停

**配置难度：** ⭐（1 分钟）
**费用：** 免费
**稳定性：** ⭐⭐⭐

#### 企业用户：云函数 ⭐⭐⭐⭐

**适合你，如果：**
- ✅ 有云服务账号
- ✅ 需要企业级稳定性
- ✅ 预算充足（虽然几乎免费）

**配置难度：** ⭐⭐⭐（20 分钟）
**费用：** ~0 元/月
**稳定性：** ⭐⭐⭐⭐⭐

---

## 🚀 快速开始 - GitHub Actions 版本

### 5 分钟配置流程

```bash
# 1. 创建 GitHub 仓库（在网页上操作）
https://github.com/new

# 2. 上传代码
cd /app/workspace/7415868573489743386/1/2/157
git init
git add .
git commit -m "初始化"
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main

# 3. 配置 Secrets（在 GitHub 网页操作）
Settings → Secrets → Actions → New secret
  - TAVILY_API_KEY
  - FEISHU_WEBHOOK_URL

# 4. 启用 Actions（在 Actions 标签页）
点击启用 → 完成！

# 5. 手动测试
Actions → 欧洲物流预警推送 → Run workflow
```

### 执行时间设置

编辑 `.github/workflows/daily_check.yml`：

```yaml
on:
  schedule:
    - cron: '0 0 * * *'   # UTC 0:00 = 北京 8:00
    - cron: '0 10 * * *'  # UTC 10:00 = 北京 18:00
```

**时区转换：**
- 北京时间 - 8 小时 = UTC 时间
- 例：北京 8:00 → UTC 0:00
- 例：北京 18:00 → UTC 10:00

---

## 🚀 快速开始 - 本地运行版本

### 1 分钟启动

```bash
# 启动程序
python3 run_local.py

# 或 Windows
python run_local.py
```

### 后台运行（Linux/Mac）

```bash
# 后台启动
nohup python3 run_local.py > logs/run.log 2>&1 &

# 查看日志
tail -f logs/run.log

# 停止程序
pkill -f run_local.py
```

### Windows 开机自动启动

1. 创建 `start.bat`：

```batch
@echo off
cd /d "你的项目路径"
python run_local.py
```

2. 将快捷方式放到：
   - Win + R → `shell:startup`

---

## 📊 方案详细对比

### GitHub Actions vs 本地运行

| 特性 | GitHub Actions | 本地运行 |
|------|----------------|----------|
| **配置难度** | 中等（10分钟） | 简单（1分钟） |
| **是否需要开机** | ❌ 不需要 | ✅ 需要 |
| **稳定性** | 非常高 | 取决于电脑 |
| **配置复杂度** | 需要 Git 和 GitHub | 直接运行 |
| **日志管理** | 自动保存 | 需手动管理 |
| **成本** | 免费 | 免费 |
| **推荐度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### 使用场景推荐

**选择 GitHub Actions，如果：**
- 你不想管理服务器
- 电脑经常关机或休眠
- 需要稳定的自动执行
- 愿意花 10 分钟学习 GitHub

**选择本地运行，如果：**
- 电脑 24 小时开机（如家庭服务器、NAS）
- 想立即使用，不想配置 GitHub
- 熟悉命令行操作
- 能接受偶尔重启程序

---

## 🔧 GitHub Actions 详细配置

### workflow 文件说明

文件位置：`.github/workflows/daily_check.yml`

**主要配置：**

```yaml
# 定时触发
on:
  schedule:
    - cron: '0 0 * * *'   # 早上 8:00（北京时间）
    - cron: '0 10 * * *'  # 晚上 18:00（北京时间）

# 手动触发（支持选择检查类型）
  workflow_dispatch:
    inputs:
      check_type:
        options:
          - both      # 天气 + 新闻
          - weather   # 仅天气
          - news      # 仅新闻
```

### 修改执行时间

如果要改变执行时间，编辑 cron 表达式：

```yaml
# 每天 6:00, 12:00, 18:00（北京时间）
- cron: '0 22 * * *'  # UTC 22:00 = 北京 6:00
- cron: '0 4 * * *'   # UTC 4:00 = 北京 12:00
- cron: '0 10 * * *'  # UTC 10:00 = 北京 18:00
```

### 数据持久化

GitHub Actions 使用 **artifacts** 保存新闻记录：
- 每次运行前下载 `sent_news.json`
- 运行后上传更新的记录
- 保留 30 天

这样可以实现去重功能！

---

## 🛠️ 本地运行详细说明

### 程序特点

- **自动定时执行** - 无需手动触发
- **保持后台运行** - 可以最小化窗口
- **资源占用低** - 仅在执行时占用资源
- **日志输出** - 实时显示执行状态

### 执行流程

```
启动程序 → 设置定时任务 → 等待执行时间
    ↓
到达 8:00 → 检查天气 → 推送飞书
    ↓
到达 9:00 → 检查新闻 → 推送飞书（如有新增）
    ↓
到达 18:00 → 检查天气 → 推送飞书
    ↓
到达 19:00 → 检查新闻 → 推送飞书（如有新增）
    ↓
循环执行...
```

### 停止程序

```bash
# 前台运行：按 Ctrl+C

# 后台运行：
pkill -f run_local.py

# 或查找进程ID后停止
ps aux | grep run_local
kill <进程ID>
```

### 开机自动启动

**Linux（systemd）：**

创建 `/etc/systemd/system/logistics-alert.service`：

```ini
[Unit]
Description=欧洲物流预警推送系统
After=network.target

[Service]
Type=simple
User=你的用户名
WorkingDirectory=/app/workspace/7415868573489743386/1/2/157
ExecStart=/usr/bin/python3 /app/workspace/7415868573489743386/1/2/157/run_local.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable logistics-alert
sudo systemctl start logistics-alert
sudo systemctl status logistics-alert
```

**Mac（launchd）：**

创建 `~/Library/LaunchAgents/com.logistics.alert.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.logistics.alert</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/你的路径/run_local.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/你的路径</string>
</dict>
</plist>
```

加载服务：

```bash
launchctl load ~/Library/LaunchAgents/com.logistics.alert.plist
```

---

## ☁️ 云函数部署（高级）

### 阿里云函数计算

#### 步骤 1：准备代码包

```bash
# 安装依赖到目录
pip install requests -t ./package

# 复制项目文件
cp *.py package/

# 打包
cd package && zip -r ../logistics-alert.zip .
```

#### 步骤 2：创建函数

1. 登录阿里云函数计算控制台
2. 创建服务
3. 创建函数：
   - 运行环境：Python 3.10
   - 上传 zip 包
   - 入口函数：`logistics_alert_github.handler`

#### 步骤 3：配置环境变量

在函数配置中添加：
- `TAVILY_API_KEY`
- `FEISHU_WEBHOOK_URL`

#### 步骤 4：创建触发器

- 类型：定时触发器
- Cron 表达式：`0 0,10 * * *`

### AWS Lambda

类似流程，使用 AWS EventBridge 设置定时触发。

---

## 📋 方案选择决策树

```
需要定时推送到飞书？
    │
    ├─ 有 GitHub 账号 or 愿意注册？
    │   └─ YES → 使用 GitHub Actions ⭐⭐⭐⭐⭐
    │
    ├─ 电脑经常开机（24小时或工作时间）？
    │   └─ YES → 使用本地运行 ⭐⭐⭐
    │
    ├─ 有云服务账号（阿里云、AWS）？
    │   └─ YES → 使用云函数 ⭐⭐⭐⭐
    │
    └─ 都不满足？
        └─ 建议注册 GitHub（免费）然后使用 Actions
```

---

## 🎯 最终推荐

### 首选：GitHub Actions

**理由：**
1. ✅ 完全免费
2. ✅ 无需服务器
3. ✅ 稳定可靠
4. ✅ 配置一次，永久使用
5. ✅ 适合长期运行

**配置时间：** 10 分钟
**月度成本：** 0 元
**维护成本：** 0

### 备选：本地运行

**理由：**
1. ✅ 立即可用
2. ✅ 配置最简单
3. ✅ 完全免费

**配置时间：** 1 分钟
**月度成本：** 0 元（仅电费）
**维护成本：** 需要偶尔检查程序运行状态

---

## 📁 相关文件

**GitHub Actions 版本：**
- `.github/workflows/daily_check.yml` - Actions 配置
- `logistics_alert_github.py` - GitHub 适配版本

**本地运行版本：**
- `run_local.py` - 本地持续运行程序

**通用版本：**
- `logistics_alert_full.py` - 适用于所有场景

---

## 🎊 总结

### 你有 3 种不需要服务器的方案

1. **GitHub Actions** - 完全免费，自动运行，最推荐 ⭐⭐⭐⭐⭐
2. **本地电脑** - 配置最简单，立即可用 ⭐⭐⭐
3. **云函数** - 企业级稳定，成本极低 ⭐⭐⭐⭐

### 立即行动

**方案 1（推荐）：**
```bash
# 上传到 GitHub → 配置 Secrets → 启用 Actions
# 详见下方 GITHUB_ACTIONS_SETUP.md
```

**方案 2（最快）：**
```bash
# 直接运行
python3 run_local.py
```

---

**下一步：** 查看 `GITHUB_ACTIONS_SETUP.md` 了解 GitHub Actions 详细配置步骤！
