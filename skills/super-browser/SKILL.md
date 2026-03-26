---
name: super-browser
description: |
  统一浏览器自动化技能，融合 AI 视觉控制、精确自动化、调试分析、内容提取四大能力。
  
  使用场景决策：
  - 自然语言操作网页 → AI 视觉模式（Midscene）
  - 精确元素定位/表单填写 → Playwright 模式
  - 性能调试/网络分析 → DevTools 模式
  - 保存网页/数据抓取 → 剪藏模式
  - 批量处理/脚本自动化 → CLI 模式
  
  触发词：打开网站、浏览器、填表单、抓数据、截图、测试网页、自动化、剪藏
allowed-tools:
  - Bash(npx @midscene/web@1:*)
  - Bash(playwright-cli:*)
  - Bash(agent-browser:*)
  - Bash
---

# 🌐 超级浏览器技能

> **统一浏览器自动化平台 — 一站式解决所有网页交互需求**

融合五大浏览器自动化能力：
- 🤖 **AI 视觉控制**（Midscene）— 自然语言操作，智能规划执行
- 🎯 **精确自动化**（Playwright）— 元素定位，表单填写，网络拦截
- 🔧 **调试分析**（DevTools）— 性能分析，网络抓包，控制台调试
- ✂️ **内容提取**（Web Clipper）— 网页剪藏，数据抓取，Markdown 转换
- ⚡ **快速操作**（agent-browser）— CLI 命令，批量处理，自动化脚本

---

## 📊 使用场景决策树

| 场景 | 推荐方式 | 工具 | 命令示例 |
|------|---------|------|---------|
| 🗣️ 自然语言操作网页 | AI 视觉 | Midscene | `npx @midscene/web@1 act --prompt "登录并下载报表"` |
| 🎯 精确元素定位 | Playwright | playwright-cli | `playwright-cli click e15` |
| 📝 表单批量填写 | Playwright | playwright-cli | `playwright-cli fill e1 "email@test.com"` |
| ⚡ 快速自动化脚本 | CLI | agent-browser | `agent-browser open url && agent-browser fill @e1 "text"` |
| 🔍 性能调试分析 | DevTools | MCP 工具 | `performance_start_trace` |
| 📡 网络抓包分析 | DevTools | MCP 工具 | `list_network_requests` |
| 💾 保存网页为 Markdown | 剪藏 | web-clipper | `python clip.py <url>` |
| 📸 批量截图 | CLI | agent-browser | `agent-browser screenshot --full` |
| 🔐 登录态持久化 | CLI | agent-browser | `agent-browser state save auth.json` |
| 📱 移动端模拟 | CLI | agent-browser | `agent-browser set device "iPhone 14"` |

---

## 🚀 快速开始

### 模式一：AI 视觉控制（推荐用于复杂交互）

```bash
# 1. 连接网页
npx @midscene/web@1 connect --url https://example.com

# 2. 截图查看当前状态
npx @midscene/web@1 take_screenshot

# 3. 自然语言操作
npx @midscene/web@1 act --prompt "点击登录按钮，填写邮箱 user@example.com 和密码 pass123，然后提交"

# 4. 关闭浏览器
npx @midscene/web@1 close
```

### 模式二：精确自动化（推荐用于表单操作）

```bash
# 1. 打开浏览器
playwright-cli open https://example.com/form

# 2. 获取页面快照（获取元素引用 e1, e2...）
playwright-cli snapshot

# 3. 精确操作元素
playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3

# 4. 关闭
playwright-cli close
```

### 模式三：快速 CLI（推荐用于脚本自动化）

```bash
# 命令链式调用
agent-browser open https://example.com && \
agent-browser snapshot -i && \
agent-browser fill @e1 "text" && \
agent-browser click @e2 && \
agent-browser screenshot result.png
```

### 模式四：调试分析

```bash
# 性能分析
playwright-cli tracing-start
# ... 执行操作 ...
playwright-cli tracing-stop

# 查看网络请求
playwright-cli network

# 查看控制台日志
playwright-cli console
```

### 模式五：网页剪藏

```bash
# 保存网页为 Markdown
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py https://example.com/article

# 带标签保存
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> --tags "技术,教程"
```

---

## 🤖 AI 视觉控制（Midscene）

### 核心优势
- ✅ 自然语言操作，无需选择器
- ✅ AI 自动规划执行步骤
- ✅ 截图识别提取数据
- ✅ 支持连接用户现有浏览器（CDP/Bridge 模式）

### 连接模式

| 模式 | 使用场景 | 前置条件 |
|------|---------|---------|
| **Puppeteer（默认）** | 新建独立浏览器 | 无 |
| **CDP 模式** | 控制用户现有 Chrome | 启用远程调试 |
| **Bridge 模式** | 通过扩展连接 | 安装 Midscene 扩展 |

### CDP 模式（连接用户浏览器）

```bash
# 预检查（端口 9222）
curl -s --max-time 2 -o /dev/null -w "%{http_code}" -H "Upgrade: websocket" http://127.0.0.1:9222/devtools/browser
# 返回 101 表示可用

# 连接
npx @midscene/web@1 connect --cdp ws://127.0.0.1:9222/devtools/browser --url https://example.com

# 操作
npx @midscene/web@1 act --cdp ws://127.0.0.1:9222/devtools/browser --prompt "点击登录按钮"

# 断开（不关闭浏览器）
npx @midscene/web@1 disconnect --cdp ws://127.0.0.1:9222/devtools/browser
```

### Bridge 模式（通过扩展）

```bash
# 预检查（端口 3766）
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://127.0.0.1:3766/socket.io/?EIO=4&transport=polling
# 返回 200/400 表示扩展监听中

# 连接
npx @midscene/web@1 --bridge connect --url https://example.com
npx @midscene/web@1 --bridge act --prompt "点击登录"
npx @midscene/web@1 --bridge disconnect
```

### act 命令能力

一次 `act` 调用可完成：
- 点击、右键、双击、悬停
- 输入、清除文本
- 按键、滚动、拖拽
- 多步骤流程（AI 自动规划）

```bash
# 复合操作示例
npx @midscene/web@1 act --prompt "滚动到底部，点击蓝色的提交按钮，等待页面加载后截图"
```

### 最佳实践

1. **批量相关操作**：将连续操作合并到一个 `act` 命令中
2. **等待加载**：导航后先截图确认页面已加载
3. **自然语言**：描述你看到的（"红色登录按钮"）而非选择器（"#login-btn"）

---

## 🎯 精确自动化（Playwright）

### 核心优势
- ✅ 精确元素定位（通过 ref 引用）
- ✅ 多页面/多标签管理
- ✅ 网络拦截和模拟
- ✅ 状态持久化（cookies、localStorage）

### 常用命令速查

```bash
# 导航
playwright-cli open <url>
playwright-cli goto <url>
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload

# 快照（获取元素引用 e1, e2...）
playwright-cli snapshot

# 交互
playwright-cli click e1
playwright-cli dblclick e1
playwright-cli fill e1 "text"
playwright-cli type "text"           # 直接输入
playwright-cli press Enter
playwright-cli hover e1
playwright-cli select e1 "option"
playwright-cli upload ./file.pdf
playwright-cli check e1

# 标签页
playwright-cli tab-new <url>
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli tab-close

# 存储
playwright-cli state-save auth.json
playwright-cli state-load auth.json
playwright-cli cookie-list
playwright-cli cookie-set name value

# 网络
playwright-cli network
playwright-cli route "**/*.jpg" --status=404

# 调试
playwright-cli console
playwright-cli tracing-start
playwright-cli tracing-stop

# 输出
playwright-cli screenshot
playwright-cli pdf output.pdf

# 关闭
playwright-cli close
```

### 表单自动化示例

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

# 填写表单
playwright-cli fill e1 "John Doe"
playwright-cli fill e2 "john@example.com"
playwright-cli select e3 "California"
playwright-cli check e4
playwright-cli click e5

# 验证结果
playwright-cli snapshot
playwright-cli close
```

### 多标签工作流

```bash
playwright-cli open https://site-a.com
playwright-cli tab-new https://site-b.com
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
playwright-cli close
```

---

## ⚡ 快速 CLI（agent-browser）

### 核心优势
- ✅ 命令链式调用，高效简洁
- ✅ 会话持久化和命名会话
- ✅ 认证保险库（加密存储密码）
- ✅ 视觉对比和差异检测
- ✅ iOS 模拟器支持

### 核心工作流

```bash
# 打开 → 快照 → 操作
agent-browser open <url>
agent-browser snapshot -i           # 获取 @e1, @e2 引用
agent-browser fill @e1 "text"
agent-browser click @e2
```

### 命令链式调用

```bash
# 一次调用完成多步操作
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot
```

### 认证保险库（推荐）

```bash
# 保存凭证（加密存储）
echo "password" | agent-browser auth save github --url https://github.com/login --username user --password-stdin

# 使用凭证登录（LLM 不接触密码）
agent-browser auth login github
```

### 会话持久化

```bash
# 命名会话（自动保存状态）
agent-browser --session-name myapp open https://app.example.com/login
# ... 登录操作 ...
agent-browser close  # 状态自动保存

# 下次自动恢复
agent-browser --session-name myapp open https://app.example.com/dashboard
```

### 视口和设备模拟

```bash
# 设置视口
agent-browser set viewport 1920 1080
agent-browser set viewport 1920 1080 2    # 2x Retina

# 设备模拟
agent-browser set device "iPhone 14"

# 暗色模式
agent-browser --color-scheme dark open https://example.com
```

### 视觉差异检测

```bash
# 快照差异
agent-browser snapshot -i
agent-browser click @e2
agent-browser diff snapshot          # 对比前后变化

# 截图差异
agent-browser screenshot baseline.png
# ... 修改 ...
agent-browser diff screenshot --baseline baseline.png
```

### iOS 模拟器

```bash
# 列出可用设备
agent-browser device list

# 启动 Safari
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com

# 移动端操作
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios swipe up

# 截图
agent-browser -p ios screenshot mobile.png
agent-browser -p ios close
```

---

## 🔧 调试分析（DevTools）

### 核心能力
- 📊 性能追踪和分析
- 📡 网络请求监控
- 🖥️ 控制台日志查看
- 🔍 JavaScript 执行

### 性能分析

```bash
# Playwright 方式
playwright-cli tracing-start
# ... 执行操作 ...
playwright-cli tracing-stop

# agent-browser 方式
agent-browser profiler start
# ... 执行操作 ...
agent-browser profiler stop trace.json
```

### 网络监控

```bash
# 查看网络请求
playwright-cli network

# 拦截请求
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
```

### 控制台调试

```bash
# 查看控制台日志
playwright-cli console
playwright-cli console warning      # 只看警告

# 执行 JavaScript
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
```

---

## ✂️ 内容提取（Web Clipper）

### 核心能力
- 💾 保存网页为 Markdown
- 🏷️ 标签分类管理
- 🔍 全文搜索
- 📚 语义搜索集成

### 基本用法

```bash
# 保存网页
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url>

# 带标签
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> --tags "技术,教程"

# Cloudflare 保护的页面
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/clip.py <url> --force-flaresolverr
```

### 管理剪藏

```bash
# 列出剪藏
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py

# 按条件筛选
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py --domain "example.com"
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/list.py --tag "python"

# 搜索
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/search.py "关键词"

# 删除
~/.claude/skills/web-clipper/.venv/bin/python ~/.claude/skills/web-clipper/scripts/delete.py <filename>
```

---

## ⚙️ 环境变量配置

### Midscene 模型配置（必需）

```bash
# Gemini 示例
MIDSCENE_MODEL_API_KEY="your-google-api-key"
MIDSCENE_MODEL_NAME="gemini-3-flash"
MIDSCENE_MODEL_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
MIDSCENE_MODEL_FAMILY="gemini"

# Qwen 示例
MIDSCENE_MODEL_API_KEY="your-aliyun-api-key"
MIDSCENE_MODEL_NAME="qwen3.5-plus"
MIDSCENE_MODEL_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
MIDSCENE_MODEL_FAMILY="qwen3.5"

# Doubao 示例
MIDSCENE_MODEL_API_KEY="your-doubao-api-key"
MIDSCENE_MODEL_NAME="doubao-seed-2-0-lite"
MIDSCENE_MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
MIDSCENE_MODEL_FAMILY="doubao-seed"
```

### agent-browser 配置（可选）

```bash
# 暗色模式
AGENT_BROWSER_COLOR_SCHEME=dark

# 超时时间（毫秒）
AGENT_BROWSER_DEFAULT_TIMEOUT=60000

# 内容边界标记（安全）
AGENT_BROWSER_CONTENT_BOUNDARIES=1

# 域名白名单
AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"

# 输出限制
AGENT_BROWSER_MAX_OUTPUT=50000

# 加密密钥（状态加密）
AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)

# 原生模式（实验性）
AGENT_BROWSER_NATIVE=1

# 浏览器引擎
AGENT_BROWSER_ENGINE=chrome  # 或 lightpanda
```

---

## 📋 最佳实践

### 1. 选择正确的工具

| 需求 | 推荐 |
|------|------|
| 复杂交互，不确定元素位置 | AI 视觉（Midscene） |
| 精确表单填写，已知元素结构 | Playwright |
| 快速脚本，批量操作 | agent-browser |
| 性能问题排查 | DevTools |
| 保存网页内容 | Web Clipper |

### 2. 状态管理

```bash
# 方式一：Playwright 状态保存
playwright-cli state-save auth.json

# 方式二：agent-browser 会话
agent-browser --session-name myapp open <url>

# 方式三：认证保险库（最安全）
agent-browser auth save site --url <url> --username user
```

### 3. 错误处理

- **页面加载慢**：使用 `wait --load networkidle`
- **元素未找到**：重新 `snapshot` 获取最新引用
- **网络问题**：使用 DevTools 检查请求
- **Cloudflare 保护**：使用 `--force-flaresolverr`

### 4. 安全建议

- ✅ 使用认证保险库存储密码
- ✅ 启用内容边界标记
- ✅ 设置域名白名单
- ✅ 加密持久化状态
- ❌ 避免在命令行直接传递密码

---

## 🔗 参考链接

| 工具 | 文档 |
|------|------|
| Midscene | https://midscenejs.com |
| Playwright | https://playwright.dev |
| agent-browser | 内置帮助 `agent-browser --help` |
| Web Clipper | 内置脚本 |

---

## 📝 更新日志

- **v1.0.0** (2026-03-26): 初始版本，融合五大浏览器自动化能力