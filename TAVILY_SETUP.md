# Tavily API 注册和配置指南

## 什么是 Tavily？

Tavily 是一个专为 AI 应用设计的搜索 API，提供实时的新闻、网页搜索能力。

**为什么选择 Tavily：**
- ✅ 专门优化用于 AI 应用
- ✅ 返回结构化的高质量结果
- ✅ 提供免费试用额度
- ✅ 支持时间范围过滤（最近24小时等）
- ✅ API 简单易用

## 注册步骤（5分钟）

### 步骤 1：访问官网

打开浏览器，访问：<a href="https://tavily.com" target="_blank">https://tavily.com</a>

### 步骤 2：注册账号

在首页点击 **"Get Started"** 或 **"Sign Up"** 按钮

**三种注册方式：**

#### 方式A：Google 账号（推荐，最快）
- 点击 "Continue with Google"
- 选择你的 Google 账号
- 授权后自动完成注册

#### 方式B：GitHub 账号
- 点击 "Continue with GitHub"
- 授权 GitHub 账号
- 自动完成注册

#### 方式C：邮箱注册
- 输入邮箱地址
- 设置密码
- 点击注册按钮
- 查收验证邮件并点击验证链接

### 步骤 3：获取 API Key

注册成功后会自动跳转到 **Dashboard**。

**在 Dashboard 页面：**
1. 你会看到 "API Key" 部分
2. API Key 已经自动生成（格式：`tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 点击 **复制** 图标复制 API Key
4. 保存到安全的地方

**重要提示：**
- ⚠️ API Key 只会显示一次，请妥善保存
- ⚠️ 不要分享给他人或提交到 Git 仓库
- 💡 如果丢失，可以在 Dashboard 重新生成

### 步骤 4：查看配额

在 Dashboard 可以看到：
- **Free Plan（免费计划）**
  - 每月 1,000 次搜索请求
  - 适合个人和小型项目
  - 无需绑定信用卡

- **使用统计**
  - 已使用次数
  - 剩余配额
  - 使用历史

**我们的需求：**
- 每天 2 次搜索（天气 + 新闻）
- 每月约 60 次
- 免费额度完全够用！

### 步骤 5：配置到项目

打开 `config.json`，填入 API Key：

```json
{
  "tavily_api_key": "tvly-你刚才复制的完整密钥",
  "feishu": {
    "webhook_url": "后续配置"
  },
  "monitoring": {
    ...
  }
}
```

### 步骤 6：测试 API Key

运行测试脚本：

```bash
python test_tavily.py
```

**预期输出：**
```
============================================================
Tavily API 测试
============================================================

🔑 API Key: tvly-xxxxx...xxxxx
📍 测试查询: 'Germany logistics weather'

正在发送请求到 Tavily API...
✅ API Key 有效！
✅ 搜索成功，返回 1 条结果

📰 示例结果:
   标题: Weather alerts issued for German logistics routes...
   URL: https://example.com/...

✅ Tavily API 配置正确，可以开始使用！
```

## 常见问题

### Q1: 注册需要付费吗？

**答：** 不需要。Tavily 提供免费计划：
- 每月 1,000 次免费搜索
- 无需绑定信用卡
- 无需订阅

### Q2: 免费额度够用吗？

**答：** 完全够用！
- 你的需求：每天 2 次搜索 = 每月 60 次
- 免费额度：每月 1,000 次
- 剩余：940 次可用于其他用途

### Q3: API Key 在哪里找？

**答：** 登录后在 Dashboard 页面：
- URL: <a href="https://app.tavily.com" target="_blank">https://app.tavily.com</a>
- 左侧菜单："API Keys" 或直接在首页显示
- 可以随时生成新的 API Key

### Q4: 配额用完了怎么办？

**答：** 有两种选择：
1. **等待下月重置** - 免费配额每月1号重置
2. **升级计划** - 如需更多配额可升级到付费计划

### Q5: API Key 丢失了怎么办？

**答：** 不用担心：
1. 登录 <a href="https://app.tavily.com" target="_blank">https://app.tavily.com</a>
2. 进入 "API Keys" 页面
3. 点击 "Regenerate" 生成新的 API Key
4. 更新 `config.json` 中的配置

### Q6: 支持哪些搜索功能？

**答：** Tavily 支持：
- ✅ 实时网页搜索
- ✅ 新闻搜索
- ✅ 时间范围过滤（24小时、一周等）
- ✅ 结果数量控制
- ✅ 多语言支持
- ✅ 搜索深度设置（basic/advanced）

### Q7: 搜索质量如何？

**答：** Tavily 专为 AI 优化：
- 返回高质量、相关性强的结果
- 自动过滤低质量内容
- 提供结构化数据（标题、URL、摘要、相关度分数）
- 比通用搜索引擎更适合程序化调用

## API 测试示例

运行我创建的测试脚本：

```bash
# 测试 Tavily API
python test_tavily.py
```

**如果成功，你会看到：**
- ✅ API Key 有效
- ✅ 搜索成功
- ✅ 返回示例结果

**如果失败，可能的原因：**
- ❌ API Key 错误 → 重新复制
- ❌ 网络问题 → 检查网络连接
- ❌ 配额用尽 → 等待重置或升级

## 完整配置示例

配置完成后，你的 `config.json` 应该是这样：

```json
{
  "tavily_api_key": "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",
  "feishu": {
    "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xyz123"
  },
  "monitoring": {
    "countries": ["Germany", "France", "Netherlands", "Belgium", "Poland"],
    "weather_keywords": [
      "extreme weather", "storm", "snow", "rain", "wind",
      "temperature", "alert", "warning"
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

## 下一步

完成 Tavily 配置后：

1. ✅ 运行 `python test_tavily.py` - 测试 API 连接
2. ✅ 运行 `python test_feishu.py` - 测试飞书推送
3. ✅ 运行 `python logistics_alert.py both` - 执行完整检查
4. ✅ 设置 cron 定时任务 - 实现自动推送

## 技术支持

**Tavily 官方资源：**
- 官网：<a href="https://tavily.com" target="_blank">https://tavily.com</a>
- Dashboard：<a href="https://app.tavily.com" target="_blank">https://app.tavily.com</a>
- API 文档：<a href="https://docs.tavily.com" target="_blank">https://docs.tavily.com</a>

**遇到问题？**
- 查看 Tavily 文档获取详细 API 说明
- 检查 Dashboard 的使用统计
- 联系 Tavily 技术支持

---

**准备就绪？** 运行 `python test_tavily.py` 开始测试！
