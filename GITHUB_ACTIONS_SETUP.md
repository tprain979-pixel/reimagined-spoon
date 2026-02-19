# GitHub Actions 部署指南（无需服务器）

## 🎯 方案概述

使用 GitHub Actions 实现：
- ✅ **完全免费** - 公开/私有仓库都支持免费额度
- ✅ **无需服务器** - GitHub 自动执行
- ✅ **自动运行** - 每天定时推送
- ✅ **稳定可靠** - GitHub 基础设施
- ✅ **日志完整** - 自动保存执行记录

---

## 📋 配置步骤（10 分钟）

### 步骤 1：创建 GitHub 仓库（2 分钟）

1. **访问 GitHub**
   - 打开 <a href="https://github.com/new" target="_blank">https://github.com/new</a>
   - 或点击右上角 "+" → "New repository"

2. **填写仓库信息**
   - Repository name: `logistics-alert-system`
   - Description: `欧洲物流天气和新闻预警推送系统`
   - 选择 **Private**（私有，保护配置安全）
   - ❌ 不要勾选 "Add a README file"
   - 点击 **"Create repository"**

3. **记录仓库地址**
   - 格式：`https://github.com/你的用户名/logistics-alert-system.git`

### 步骤 2：上传项目代码（3 分钟）

在项目目录执行：

```bash
# 切换到项目目录
cd /app/workspace/7415868573489743386/1/2/157

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化欧洲物流预警系统

- 天气预警监控（每日推送）
- 物流新闻监控（增量推送）
- 中英文双语推送
- 自动去重功能"

# 设置默认分支为 main
git branch -M main

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/logistics-alert-system.git

# 推送代码
git push -u origin main
```

**如果提示需要登录：**

```bash
# 配置 Git 用户信息
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 使用 Personal Access Token 登录
# 访问 https://github.com/settings/tokens
# 生成 token 后使用 token 作为密码
```

### 步骤 3：配置 GitHub Secrets（2 分钟）

**⚠️ 重要：不要将密钥提交到代码中！**

1. **打开仓库设置**
   - 访问你的仓库页面
   - 点击 **Settings** 标签

2. **进入 Secrets 配置**
   - 左侧菜单：**Secrets and variables** → **Actions**

3. **添加 Secret 1: Tavily API Key**
   - 点击 **"New repository secret"**
   - Name: `TAVILY_API_KEY`
   - Secret: `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`
   - 点击 **"Add secret"**

4. **添加 Secret 2: 飞书 Webhook**
   - 再次点击 **"New repository secret"**
   - Name: `FEISHU_WEBHOOK_URL`
   - Secret: `https://open.feishu.cn/open-apis/bot/v2/hook/a14fed8b-a114-429a-8c14-c54db1666c97`
   - 点击 **"Add secret"**

5. **验证 Secrets**
   - 确认看到 2 个 secrets
   - ✅ `TAVILY_API_KEY`
   - ✅ `FEISHU_WEBHOOK_URL`

### 步骤 4：启用 GitHub Actions（1 分钟）

1. **进入 Actions 页面**
   - 点击仓库的 **Actions** 标签

2. **启用 Workflows**
   - 如果显示 "Workflows aren't being run on this repository"
   - 点击 **"I understand my workflows, go ahead and enable them"**

3. **查看工作流**
   - 左侧应该显示：**"欧洲物流预警推送"**
   - 点击查看详情

### 步骤 5：手动测试（2 分钟）

1. **触发工作流**
   - 在 Actions 页面，点击左侧 **"欧洲物流预警推送"**
   - 点击右上角 **"Run workflow"** 按钮
   - 选择分支：`main`
   - 检查类型：`both`
   - 点击 **"Run workflow"**

2. **查看执行过程**
   - 刷新页面，看到新的执行记录
   - 点击执行记录
   - 查看 "weather-alert" 和 "news-alert" 任务

3. **查看日志**
   - 点击任务名称展开
   - 查看每个步骤的输出

4. **验证推送**
   - 查看飞书群聊
   - 应该收到天气和新闻推送消息

### 步骤 6：等待自动执行

**完成！** GitHub Actions 会自动：
- ⏰ 每天早上 8:00（北京时间）执行
- ⏰ 每天晚上 18:00（北京时间）执行
- 📱 自动推送到飞书

---

## 🕐 执行时间配置

### 当前配置

```yaml
schedule:
  - cron: '0 0 * * *'   # UTC 0:00 = 北京 8:00
  - cron: '0 10 * * *'  # UTC 10:00 = 北京 18:00
```

### 时区转换表

| 北京时间 | UTC 时间 | Cron 表达式 |
|----------|----------|-------------|
| 06:00 | 22:00 (前一天) | `0 22 * * *` |
| 08:00 | 00:00 | `0 0 * * *` |
| 09:00 | 01:00 | `0 1 * * *` |
| 12:00 | 04:00 | `0 4 * * *` |
| 18:00 | 10:00 | `0 10 * * *` |
| 21:00 | 13:00 | `0 13 * * *` |

### 修改执行时间

编辑 `.github/workflows/daily_check.yml`：

```yaml
# 每天 3 次：早中晚
schedule:
  - cron: '0 0 * * *'   # 北京 8:00
  - cron: '0 4 * * *'   # 北京 12:00
  - cron: '0 10 * * *'  # 北京 18:00
```

修改后：
```bash
git add .github/workflows/daily_check.yml
git commit -m "更新执行时间"
git push
```

---

## 📊 GitHub Actions 配额

### 免费额度

**公开仓库：**
- ✅ 无限制使用

**私有仓库（你的情况）：**
- ✅ 每月 2,000 分钟免费
- ✅ 超出后 $0.008/分钟

### 你的使用量

**每次执行：**
- 天气检查：~30 秒
- 新闻检查：~30 秒
- 合计：~1 分钟

**每天 2 次：**
- 每天：2 分钟
- 每月：60 分钟
- **配额占用：** 3%

**剩余：** 1,940 分钟可用于其他项目

### 结论

✅ **完全够用，不用担心！**

---

## 🔍 查看执行日志

### 在 GitHub 查看

1. 打开仓库 → **Actions** 标签
2. 点击任意执行记录
3. 查看详细步骤：
   - ✅ 安装依赖
   - ✅ 执行天气检查
   - ✅ 执行新闻检查
   - ✅ 推送结果

### 下载日志

1. 在执行记录页面
2. 右上角 **Artifacts** 部分
3. 下载 `weather-log` 或 `news-log`

---

## 🔧 高级配置

### 自定义执行频率

**每天 3 次：**
```yaml
schedule:
  - cron: '0 0 * * *'   # 北京 8:00
  - cron: '0 4 * * *'   # 北京 12:00
  - cron: '0 10 * * *'  # 北京 18:00
```

**每天 4 次：**
```yaml
schedule:
  - cron: '0 0 * * *'   # 北京 8:00
  - cron: '0 2 * * *'   # 北京 10:00
  - cron: '0 6 * * *'   # 北京 14:00
  - cron: '0 10 * * *'  # 北京 18:00
```

### 添加通知

**执行失败时发送邮件：**

在 workflow 中添加：

```yaml
      - name: 通知失败
        if: failure()
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: 物流预警系统执行失败
          to: your-email@example.com
          from: GitHub Actions
          body: 请检查 Actions 日志
```

---

## 🐛 故障排查

### 问题 1：Actions 没有执行

**检查：**
1. Actions 是否已启用（Actions 标签页）
2. Workflow 文件路径是否正确（`.github/workflows/`）
3. Cron 时间是否已到

**注意：** GitHub Actions 的 cron 可能有 5-10 分钟的延迟。

### 问题 2：推送失败

**检查：**
1. Secrets 是否配置正确
2. 查看 Actions 日志中的错误信息
3. 测试飞书 Webhook 是否有效

### 问题 3：新闻重复推送

**原因：** GitHub Actions 每次运行都是新环境

**解决：** 使用 artifacts 保存 `sent_news.json`
- ✅ 已在 workflow 中配置
- 每次运行前下载
- 运行后上传

---

## 📖 完整命令参考

### 初始化 Git

```bash
cd /app/workspace/7415868573489743386/1/2/157
git init
git add .
git commit -m "初始化"
git branch -M main
git remote add origin https://github.com/你的用户名/logistics-alert-system.git
git push -u origin main
```

### 更新代码

```bash
git add .
git commit -m "更新配置"
git push
```

### 手动触发

在 GitHub Actions 页面点击 "Run workflow"

---

## 🎉 完成！

### GitHub Actions 优势总结

1. ✅ **零成本** - 完全免费
2. ✅ **零维护** - 无需管理服务器
3. ✅ **高可用** - GitHub 基础设施
4. ✅ **易监控** - Web 界面查看日志
5. ✅ **易调试** - 手动触发测试
6. ✅ **安全** - Secrets 加密存储

### 下一步

1. 创建 GitHub 仓库
2. 上传代码
3. 配置 Secrets
4. 手动测试
5. 等待自动执行

---

**准备好了吗？** 现在就创建 GitHub 仓库开始部署！ 🚀
