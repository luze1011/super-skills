# Playwright 自动化参考

> Playwright 是微软开发的浏览器自动化工具，支持精确元素定位和多浏览器测试。

## 目录

1. [命令速查](#命令速查)
2. [元素定位](#元素定位)
3. [交互操作](#交互操作)
4. [状态管理](#状态管理)
5. [网络控制](#网络控制)
6. [调试工具](#调试工具)

---

## 命令速查

### 导航命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `open` | 打开浏览器 | `playwright-cli open https://example.com` |
| `goto` | 导航到 URL | `playwright-cli goto https://example.com/page` |
| `go-back` | 后退 | `playwright-cli go-back` |
| `go-forward` | 前进 | `playwright-cli go-forward` |
| `reload` | 刷新 | `playwright-cli reload` |

### 快照和元素

| 命令 | 功能 | 示例 |
|------|------|------|
| `snapshot` | 获取页面快照 | `playwright-cli snapshot` |
| `click` | 点击元素 | `playwright-cli click e1` |
| `fill` | 填写文本 | `playwright-cli fill e1 "text"` |
| `type` | 输入文本 | `playwright-cli type "text"` |
| `press` | 按键 | `playwright-cli press Enter` |

---

## 元素定位

### 快照引用

Playwright CLI 使用 `snapshot` 命令生成页面快照，并为每个可交互元素分配引用 ID：

```
e1: [button] "登录"
e2: [textbox] "邮箱"
e3: [textbox] "密码"
e4: [link] "忘记密码？"
```

### 定位方式

```bash
# 1. 通过引用 ID（推荐）
playwright-cli click e1

# 2. 通过选择器
playwright-cli click "#login-btn"
playwright-cli click "text=登录"
playwright-cli click "[data-testid='submit']"

# 3. 通过文本
playwright-cli click "text=提交"
playwright-cli click "text=/提交|确认/i"  # 正则
```

---

## 交互操作

### 点击操作

```bash
# 普通点击
playwright-cli click e1

# 双击
playwright-cli dblclick e1

# 右键点击
playwright-cli click e1 --button right

# 点击并等待
playwright-cli click e1 --wait-for load
```

### 输入操作

```bash
# 清空并填写
playwright-cli fill e1 "text"

# 追加输入
playwright-cli type "more text"

# 慢速输入（模拟真人）
playwright-cli type "text" --delay 100

# 上传文件
playwright-cli upload ./file.pdf
```

### 表单操作

```bash
# 选择下拉选项
playwright-cli select e1 "option-value"
playwright-cli select e1 "text=显示文本"

# 勾选复选框
playwright-cli check e1
playwright-cli uncheck e1
```

### 按键操作

```bash
# 单键
playwright-cli press Enter
playwright-cli press Escape
playwright-cli press Tab

# 组合键
playwright-cli press "Control+A"
playwright-cli press "Control+C"
playwright-cli press "Meta+Shift+K"
```

### 其他操作

```bash
# 悬停
playwright-cli hover e1

# 焦点
playwright-cli focus e1

# 滚动
playwright-cli eval "el => el.scrollIntoView()" e1
```

---

## 状态管理

### 保存和加载状态

```bash
# 保存当前登录状态
playwright-cli state-save auth.json

# 加载状态（自动恢复 cookies、localStorage）
playwright-cli state-load auth.json
```

### Cookie 管理

```bash
# 列出 cookies
playwright-cli cookie-list

# 设置 cookie
playwright-cli cookie-set name value

# 设置带属性的 cookie
playwright-cli cookie-set session_id "abc123" \
  --domain ".example.com" \
  --path "/" \
  --secure
```

---

## 网络控制

### 查看网络请求

```bash
# 列出所有请求
playwright-cli network

# 筛选请求
playwright-cli network --filter "api"
```

### 拦截请求

```bash
# 拦截并返回 404
playwright-cli route "**/*.jpg" --status=404

# 拦截并返回模拟数据
playwright-cli route "https://api.example.com/**" \
  --body='{"mock": true}'

# 拦截并修改响应
playwright-cli route "**/api/data" \
  --body='{"modified": true}' \
  --content-type="application/json"

# 清除路由
playwright-cli route-clear
```

### 等待网络

```bash
# 等待特定请求
playwright-cli wait --request "**/api/data"

# 等待响应
playwright-cli wait --response "**/api/data"
```

---

## 调试工具

### 控制台

```bash
# 查看所有日志
playwright-cli console

# 只看错误
playwright-cli console error

# 只看警告
playwright-cli console warning
```

### 性能追踪

```bash
# 开始追踪
playwright-cli tracing-start

# 执行操作...

# 停止并保存
playwright-cli tracing-stop

# 查看追踪文件
# 用 Chromium 打开 trace.zip
```

### 执行 JavaScript

```bash
# 获取值
playwright-cli eval "document.title"

# 使用元素引用
playwright-cli eval "el => el.textContent" e1

# 复杂操作
playwright-cli eval "
  const elements = document.querySelectorAll('.item');
  return Array.from(elements).map(el => el.textContent);
"
```

---

## 多标签/多页面

### 标签管理

```bash
# 新建标签
playwright-cli tab-new https://example.com

# 列出所有标签
playwright-cli tab-list

# 切换标签（索引从 0 开始）
playwright-cli tab-select 0
playwright-cli tab-select 1

# 关闭当前标签
playwright-cli tab-close

# 关闭其他标签
playwright-cli tab-close-others
```

---

## 输出

### 截图

```bash
# 可见区域截图
playwright-cli screenshot page.png

# 全页截图
playwright-cli screenshot full.png --full-page

# 特定元素
playwright-cli screenshot element.png --element e1
```

### PDF

```bash
# 生成 PDF
playwright-cli pdf output.pdf

# 带参数
playwright-cli pdf output.pdf \
  --format A4 \
  --landscape \
  --print-background
```

---

## 参考链接

- 官方文档：https://playwright.dev
- CLI 文档：https://playwright.dev/python/docs/cli