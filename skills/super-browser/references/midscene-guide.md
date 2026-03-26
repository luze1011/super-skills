# Midscene AI 视觉控制指南

> Midscene.js 是一个 AI 驱动的浏览器自动化工具，让用户可以用自然语言控制网页。

## 目录

1. [核心概念](#核心概念)
2. [连接模式](#连接模式)
3. [act 命令详解](#act-命令详解)
4. [数据提取](#数据提取)
5. [最佳实践](#最佳实践)

---

## 核心概念

### 什么是 Midscene？

Midscene 使用 AI 视觉模型理解页面内容，用户只需描述"做什么"，而非"怎么定位"。

**传统方式**：
```javascript
await page.click('#login-btn');
await page.fill('input[name="email"]', 'user@example.com');
```

**Midscene 方式**：
```bash
npx @midscene/web@1 act --prompt "点击登录按钮，填写邮箱 user@example.com"
```

### 核心命令

| 命令 | 功能 |
|------|------|
| `connect` | 连接到网页 |
| `act` | 执行自然语言操作 |
| `extract` | 提取页面数据 |
| `take_screenshot` | 截图 |
| `close` | 关闭浏览器 |

---

## 连接模式

### 1. Puppeteer 模式（默认）

新建独立浏览器实例：

```bash
npx @midscene/web@1 connect --url https://example.com
```

### 2. CDP 模式

连接用户现有的 Chrome 浏览器：

```bash
# 1. 启动 Chrome（启用远程调试）
chrome --remote-debugging-port=9222

# 2. 检查端口可用性
curl -s --max-time 2 -o /dev/null -w "%{http_code}" \
  -H "Upgrade: websocket" \
  http://127.0.0.1:9222/devtools/browser
# 返回 101 表示可用

# 3. 连接
npx @midscene/web@1 connect \
  --cdp ws://127.0.0.1:9222/devtools/browser \
  --url https://example.com

# 4. 操作
npx @midscene/web@1 act --cdp ws://127.0.0.1:9222/devtools/browser \
  --prompt "点击登录"

# 5. 断开（不关闭浏览器）
npx @midscene/web@1 disconnect --cdp ws://127.0.0.1:9222/devtools/browser
```

### 3. Bridge 模式

通过浏览器扩展连接：

```bash
# 1. 安装 Midscene 浏览器扩展

# 2. 检查扩展端口
curl -s --max-time 2 -o /dev/null -w "%{http_code}" \
  "http://127.0.0.1:3766/socket.io/?EIO=4&transport=polling"
# 返回 200/400 表示扩展监听中

# 3. 连接
npx @midscene/web@1 --bridge connect --url https://example.com
```

---

## act 命令详解

### 基本语法

```bash
npx @midscene/web@1 act --prompt "操作描述"
```

### 支持的操作

| 操作类型 | 示例 |
|---------|------|
| 点击 | "点击登录按钮"、"点击红色的提交按钮" |
| 输入 | "在搜索框输入 hello world" |
| 按键 | "按回车键"、"按 Escape" |
| 滚动 | "滚动到底部"、"向下滚动一屏" |
| 悬停 | "悬停在用户头像上" |
| 拖拽 | "拖拽文件到上传区域" |
| 等待 | "等待页面加载完成" |
| 组合操作 | "点击登录，填写邮箱，点击提交" |

### 批量操作

将相关操作合并到一个 prompt 中：

```bash
# ✅ 推荐：批量相关操作
npx @midscene/web@1 act --prompt "
  在搜索框输入 'playwright'，
  点击搜索按钮，
  等待结果加载，
  点击第一个结果
"

# ❌ 不推荐：分开调用
npx @midscene/web@1 act --prompt "在搜索框输入 'playwright'"
npx @midscene/web@1 act --prompt "点击搜索按钮"
npx @midscene/web@1 act --prompt "点击第一个结果"
```

### 元素描述技巧

描述你看到的，而非选择器：

```bash
# ✅ 好的描述
"点击蓝色的提交按钮"
"在标有 Email 的输入框中填写 user@example.com"
"点击右上角的用户头像"
"点击第一个搜索结果"

# ❌ 不好的描述（依赖选择器知识）
"点击 #submit-btn"
"在 input[name='email'] 中填写..."
"点击 .avatar-button"
```

---

## 数据提取

### extract 命令

从页面提取结构化数据：

```bash
# 提取商品列表
npx @midscene/web@1 extract --prompt "提取所有商品的名称、价格和评分"

# 提取特定信息
npx @midscene/web@1 extract --prompt "提取页面中的所有链接"
```

### 输出格式

Midscene 自动将提取结果格式化为 JSON。

---

## 最佳实践

### 1. 截图确认

导航后先截图确认页面状态：

```bash
npx @midscene/web@1 connect --url https://example.com
npx @midscene/web@1 take_screenshot
# 查看截图，确认页面加载完成
npx @midscene/web@1 act --prompt "..."
```

### 2. 等待策略

在 prompt 中包含等待指令：

```bash
npx @midscene/web@1 act --prompt "
  点击加载更多按钮，
  等待新内容加载完成，
  截图
"
```

### 3. 错误恢复

如果操作失败，重新截图并尝试：

```bash
npx @midscene/web@1 take_screenshot
# 分析当前状态
npx @midscene/web@1 act --prompt "..."  # 重试
```

### 4. 模型配置

配置 AI 模型以获得最佳效果：

```bash
# Gemini（推荐）
export MIDSCENE_MODEL_API_KEY="your-google-api-key"
export MIDSCENE_MODEL_NAME="gemini-3-flash"
export MIDSCENE_MODEL_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
export MIDSCENE_MODEL_FAMILY="gemini"

# Qwen
export MIDSCENE_MODEL_API_KEY="your-aliyun-api-key"
export MIDSCENE_MODEL_NAME="qwen3.5-plus"
export MIDSCENE_MODEL_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MIDSCENE_MODEL_FAMILY="qwen3.5"

# Doubao
export MIDSCENE_MODEL_API_KEY="your-doubao-api-key"
export MIDSCENE_MODEL_NAME="doubao-seed-2-0-lite"
export MIDSCENE_MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export MIDSCENE_MODEL_FAMILY="doubao-seed"
```

---

## 参考链接

- 官方文档：https://midscenejs.com
- GitHub：https://github.com/web-infra-dev/midscene