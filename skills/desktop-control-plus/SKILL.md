---
name: desktop-control-plus
description: |
  增强版桌面自动化技能 - 融合精确坐标控制与 AI 视觉驱动能力。
  
  双引擎架构：
  - PyAutoGUI 引擎：精确坐标控制、图像定位、键盘快捷键
  - Midscene 引擎：自然语言指令、AI 视觉理解、智能交互
  
  ⚠️ 警告：此技能会接管用户的鼠标和键盘。自动化运行期间用户无法操作电脑。
  → Web 应用优先使用 Browser Automation 技能（无头浏览器，不影响用户操作）
  → 仅用于桌面原生应用（Electron、Qt、原生 macOS/Windows/Linux 应用）

  触发词：桌面控制、鼠标点击、键盘输入、屏幕截图、自动化测试、桌面应用测试、
  打开应用、切换窗口、表单填写、UI 自动化、屏幕识别、OCR、图像定位
  
allowed-tools:
  - Bash
---

# Desktop Control Plus - 增强版桌面自动化

> **关键规则 — 违反将导致工作流失败：**
>
> 1. **Midscene 命令必须同步运行** — 不能后台执行，每个命令必须等待完成
> 2. **一次只运行一个 Midscene 命令** — 等待上一个完成，读取截图，再决定下一步
> 3. **给足够时间完成** — Midscene 涉及 AI 推理，典型命令需要约 1 分钟
> 4. **完成后必须报告结果** — 包括关键数据、完成的操作、截图路径等

## 双引擎架构

| 引擎 | 工具 | 优势 | 适用场景 |
|------|------|------|---------|
| **精确控制引擎** | `uvx desktop-agent` | 坐标精确、速度快、图像识别 | 表单填写、快捷键操作、精确点击 |
| **智能视觉引擎** | `npx @midscene/computer@1` | 自然语言、AI 理解、自动处理 | 复杂 UI 交互、目标驱动任务 |

---

## 一、精确控制引擎（PyAutoGUI）

### 命令结构

```bash
uvx desktop-agent <category> <command> [arguments] [options]
```

**分类：**
- `mouse` - 鼠标控制
- `keyboard` - 键盘输入
- `screen` - 截图和屏幕分析
- `message` - 用户对话框
- `app` - 应用程序控制

---

### 🖱️ 鼠标控制

```bash
# 移动鼠标到坐标
uvx desktop-agent mouse move <x> <y> [--duration SECONDS]

# 点击
uvx desktop-agent mouse click [x] [y] [--button left|right|middle] [--clicks N]
uvx desktop-agent mouse double-click [x] [y]
uvx desktop-agent mouse right-click [x] [y]

# 拖拽
uvx desktop-agent mouse drag <x> <y> [--duration SECONDS] [--button BUTTON]

# 滚轮（正数=上，负数=下）
uvx desktop-agent mouse scroll <clicks> [x] [y]

# 获取当前位置
uvx desktop-agent mouse position
```

**示例：**
```bash
# 移动到屏幕中心（1920x1080）
uvx desktop-agent mouse move 960 540 --duration 0.5

# 右键点击
uvx desktop-agent mouse right-click 500 300

# 向下滚动 5 格
uvx desktop-agent mouse scroll -5
```

---

### ⌨️ 键盘控制

```bash
# 输入文本
uvx desktop-agent keyboard write "<text>" [--interval SECONDS]

# 按键
uvx desktop-agent keyboard press <key> [--presses N] [--interval SECONDS]

# 快捷键组合（逗号分隔）
uvx desktop-agent keyboard hotkey "<key1>,<key2>,..."

# 按住/释放
uvx desktop-agent keyboard keydown <key>
uvx desktop-agent keyboard keyup <key>
```

**常用键名：**
- 修饰键：`ctrl`, `shift`, `alt`, `win` (Windows) / `command` (macOS)
- 特殊键：`enter`, `tab`, `esc`, `space`, `backspace`, `delete`
- 功能键：`f1` - `f12`
- 方向键：`up`, `down`, `left`, `right`

**示例：**
```bash
# 自然延迟输入
uvx desktop-agent keyboard write "Hello World" --interval 0.05

# 复制
uvx desktop-agent keyboard hotkey "ctrl,c"

# 打开任务管理器
uvx desktop-agent keyboard hotkey "ctrl,shift,esc"

# 连续按 3 次 Enter
uvx desktop-agent keyboard press enter --presses 3
```

---

### 🖼️ 屏幕与截图

```bash
# 截图
uvx desktop-agent screen screenshot <filename> [--region "x,y,width,height"] [--window <title>] [--active]

# 图像定位
uvx desktop-agent screen locate <image_path> [--confidence 0.0-1.0] [--window <title>]
uvx desktop-agent screen locate-center <image_path> [--confidence 0.0-1.0] [--window <title>]

# OCR 文字定位
uvx desktop-agent screen locate-text-coordinates <text> [--window <title>] [--active]
uvx desktop-agent screen read-all-text [--window <title>] [--active]

# 工具命令
uvx desktop-agent screen pixel <x> <y>
uvx desktop-agent screen size
uvx desktop-agent screen on-screen <x> <y>
```

**示例：**
```bash
# 活动窗口截图
uvx desktop-agent screen screenshot active.png --active

# 指定应用截图
uvx desktop-agent screen screenshot chrome.png --window "Google Chrome"

# 在记事本中定位图像
uvx desktop-agent screen locate-center button.png --window "Notepad"
```

---

### 📱 应用程序控制

```bash
# 打开应用
uvx desktop-agent app open <name> [--arg ARGS...]

# 聚焦窗口
uvx desktop-agent app focus <name>

# 列出所有窗口
uvx desktop-agent app list
```

**示例：**
```bash
# Windows: 打开记事本
uvx desktop-agent app open notepad

# 打开 Chrome 并访问 URL
uvx desktop-agent app open "chrome" --arg "https://google.com"

# macOS: 打开 Safari
uvx desktop-agent app open "Safari"

# 列出所有窗口
uvx desktop-agent app list
```

---

### 💬 用户对话框

```bash
# 警告框
uvx desktop-agent message alert "<text>" [--title TITLE]

# 确认框
uvx desktop-agent message confirm "<text>" [--title TITLE] [--buttons "OK,Cancel"]

# 输入框
uvx desktop-agent message prompt "<text>" [--title TITLE] [--default TEXT]

# 密码框
uvx desktop-agent message password "<text>" [--title TITLE]
```

---

## 二、智能视觉引擎（Midscene）

> **GitHub**: https://github.com/web-infra-dev/midscene
> **文档**: https://midscenejs.com
> **Stars**: 12k+

### 什么是 Midscene？

Midscene.js 是 **AI 驱动、视觉优先的 UI 自动化工具**：
- 🧠 用自然语言描述任务，AI 自动规划执行
- 👁️ 纯视觉定位，不依赖 DOM
- 🖥️ 支持 Web、Android、iOS、桌面全平台

### 核心优势

| 优势 | 说明 |
|------|------|
| **自然语言** | "打开记事本，输入 Hello" → AI 自动执行 |
| **智能理解** | 不需要坐标，AI 看图理解 UI |
| **跨平台** | Windows/macOS/Linux/Android/iOS |
| **开源模型** | Qwen-VL、UI-TARS 可本地部署 |

---

### 前置条件

需要配置支持视觉定位的模型。**已配置 Qwen3.5 Plus**。

```bash
# 环境变量（已配置在用户环境变量中）
MIDSCENE_MODEL_API_KEY="sk-sp-fe2b..."     # Qwen API Key
MIDSCENE_MODEL_NAME="qwen3.5-plus"         # 模型名称
MIDSCENE_MODEL_BASE_URL="https://coding.dashscope.aliyuncs.com/v1"
MIDSCENE_MODEL_FAMILY="qwen3.5"
MIDSCENE_MODEL_REASONING_ENABLED="false"   # 关闭思考模式加速执行
```

> ⚠️ **重要**：如果 Midscene 报错 "model name is required"，需要在当前 PowerShell 会话中设置环境变量：
> ```powershell
> $env:MIDSCENE_MODEL_API_KEY = "sk-sp-fe2b1e4bcf2247f4b7aa0994832e9f42"
> $env:MIDSCENE_MODEL_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
> $env:MIDSCENE_MODEL_NAME = "qwen3.5-plus"
> $env:MIDSCENE_MODEL_FAMILY = "qwen3.5"
> $env:MIDSCENE_MODEL_REASONING_ENABLED = "false"
> ```
> 
> 或使用初始化脚本：
> ```powershell
> . .\skills\desktop-control-plus\scripts\init-midscene.ps1
> ```

**推荐模型：** Doubao Seed 2.0 Lite, Qwen 3.5 ✅, Zhipu GLM-4.6V, Gemini-3-Pro

---

### 命令

```bash
# 连接桌面
npx @midscene/computer@1 connect
npx @midscene/computer@1 connect --displayId <id>

# 列出显示器
npx @midscene/computer@1 list_displays

# 截图
npx @midscene/computer@1 take_screenshot

# 执行动作（自然语言）
npx @midscene/computer@1 act --prompt "在搜索框输入 hello world 并按回车"

# 断开连接
npx @midscene/computer@1 disconnect
```

---

### act 命令详解

`act` 是核心命令，用自然语言描述想要完成的任务：

```bash
# 具体指令
npx @midscene/computer@1 act --prompt "在搜索框输入 hello world 并按回车"
npx @midscene/computer@1 act --prompt "将文件图标拖到回收站"

# 目标驱动指令
npx @midscene/computer@1 act --prompt "使用 Chrome 浏览器搜索上海的天气，告诉我结果"
```

**重要：** 将相关操作合并到单个 `act` 命令中，而不是拆分成多个命令。

---

### 🎯 提示词技巧

**好的提示词**：
```bash
# ✅ 清晰具体
"打开记事本，输入 Hello World，保存到桌面，文件名 test.txt"
"在 Chrome 中搜索 Midscene GitHub，打开第一个结果"
"打开设置，找到关于本机，查看系统版本"

# ✅ 包含验证条件
"填写注册表单，确保所有字段通过验证，但不要真正提交"
```

**不好的提示词**：
```bash
# ❌ 太模糊
"搜索一下"
"帮我做这个"

# ❌ 缺少关键信息
"打开那个应用"  # 哪个应用？
"输入一些文字"  # 输入什么？
```

---

### ⚡ deepThink 模式

复杂任务启用深度思考，提高成功率：

```bash
# 复杂表单填写
npx @midscene/computer@1 act --prompt "完成 GitHub 注册表单，确保所有字段通过验证" --deepThink

# 多步骤操作
npx @midscene/computer@1 act --prompt "登录电商网站，搜索商品，加入购物车" --deepThink
```

**支持的模型**：qwen3.5、qwen3-vl、doubao-seed、glm-v

---

### 📊 查看执行报告

每次执行后生成可视化 HTML 报告：

```
./midscene_run/report/computer-YYYY-MM-DD_HH-MM-SS-xxx.html
```

报告包含：
- 执行步骤截图
- AI 规划过程
- 执行时间统计
- 错误信息（如有）

---

## 三、工作流程模式

### 模式 A：精确控制流程

适用于需要精确坐标或图像识别的任务。

```bash
# 1. 获取屏幕尺寸
uvx desktop-agent screen size

# 2. 列出窗口
uvx desktop-agent app list

# 3. 打开/聚焦应用
uvx desktop-agent app open notepad
uvx desktop-agent app focus "Notepad"

# 4. 执行操作
uvx desktop-agent keyboard write "Hello World"
uvx desktop-agent keyboard hotkey "ctrl,s"
```

---

### 模式 B：智能视觉流程

适用于复杂 UI 交互或目标驱动的任务。

```bash
# 1. 连接桌面
npx @midscene/computer@1 connect

# 2. 健康检查（观察 connect 输出，如果已做健康检查则跳过）
npx @midscene/computer@1 take_screenshot
npx @midscene/computer@1 act --prompt "将鼠标移动到随机位置"

# 3. 启动目标应用并截图确认
npx @midscene/computer@1 act --prompt "打开 Safari 浏览器"
npx @midscene/computer@1 take_screenshot

# 4. 执行动作
npx @midscene/computer@1 act --prompt "在地址栏输入 github.com 并访问"

# 5. 断开连接
npx @midscene/computer@1 disconnect

# 6. 报告结果
```

---

### 模式 C：混合流程（推荐）

结合两种引擎的优势：

```bash
# 阶段1：使用精确控制打开应用
uvx desktop-agent app open "Google Chrome"

# 阶段2：使用智能视觉执行复杂操作
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "在 Chrome 中搜索 Python 教程，打开第一个结果"
npx @midscene/computer@1 take_screenshot
npx @midscene/computer@1 disconnect

# 阶段3：使用精确控制执行快捷键操作
uvx desktop-agent keyboard hotkey "ctrl,s"
```

---

## 四、常用自动化场景

### 场景1：打开应用并输入

```bash
# 精确控制方式
uvx desktop-agent app open notepad
uvx desktop-agent app focus "Notepad"
uvx desktop-agent keyboard write "Hello from Desktop Control Plus!"
```

### 场景2：截图与分析

```bash
# 获取屏幕尺寸
uvx desktop-agent screen size

# 截取活动窗口
uvx desktop-agent screen screenshot active.png --active

# 检查 UI 元素是否可见
uvx desktop-agent screen locate save_button.png --confidence 0.8
```

### 场景3：表单填写

```bash
# 点击第一个字段
uvx desktop-agent mouse click 300 200

# 填写字段
uvx desktop-agent keyboard write "张三"

# Tab 到下一个字段
uvx desktop-agent keyboard press tab
uvx desktop-agent keyboard write "zhang@example.com"

# 提交表单
uvx desktop-agent keyboard press enter
```

### 场景4：复制粘贴操作

```bash
# 全选
uvx desktop-agent keyboard hotkey "ctrl,a"

# 复制
uvx desktop-agent keyboard hotkey "ctrl,c"

# 点击目标位置
uvx desktop-agent mouse click 500 600

# 粘贴
uvx desktop-agent keyboard hotkey "ctrl,v"
```

### 场景5：图像定位与点击

```bash
# 定位图像中心点
uvx desktop-agent screen locate-center button.png --confidence 0.8

# 使用返回的坐标点击
uvx desktop-agent mouse click 125 215
```

### 场景6：OCR 文字定位

```bash
# 读取屏幕所有文字
uvx desktop-agent screen read-all-text --active

# 定位特定文字
uvx desktop-agent screen locate-text-coordinates "保存" --active

# 使用返回的坐标点击
uvx desktop-agent mouse click <x> <y>
```

### 场景7：复杂 UI 交互（Midscene）

```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "在 Word 中打开最近文档，将第一段文字复制到剪贴板"
npx @midscene/computer@1 take_screenshot
npx @midscene/computer@1 disconnect
```

---

## 五、决策指南

```
需要与桌面应用交互？
├── 精确坐标已知 → 精确控制引擎 (uvx desktop-agent)
├── 需要图像识别 → 精确控制引擎 (screen locate)
├── 需要 OCR → 精确控制引擎 (screen locate-text-coordinates)
├── 需要快捷键 → 精确控制引擎 (keyboard hotkey)
├── 复杂 UI 交互 → 智能视觉引擎 (midscene act)
├── 目标驱动任务 → 智能视觉引擎 (midscene act)
└── 混合需求 → 混合流程
```

---

## 六、平台特定注意事项

### Windows

```bash
# 常用快捷键
uvx desktop-agent keyboard hotkey "win,d"        # 显示桌面
uvx desktop-agent keyboard hotkey "win,e"        # 打开资源管理器
uvx desktop-agent keyboard hotkey "alt,tab"      # 切换窗口
uvx desktop-agent keyboard hotkey "win,r"        # 运行对话框

# 打开应用
uvx desktop-agent app open notepad
uvx desktop-agent app open calc
uvx desktop-agent app open mspaint
```

### macOS

```bash
# 常用快捷键（使用 'command' 表示 Cmd 键）
uvx desktop-agent keyboard hotkey "command,space"   # Spotlight
uvx desktop-agent keyboard hotkey "command,tab"     # 应用切换
uvx desktop-agent keyboard hotkey "command,q"       # 退出应用
uvx desktop-agent keyboard hotkey "command,shift,3" # 截图

# 打开应用
uvx desktop-agent app open "Safari"
uvx desktop-agent app open "TextEdit"

# macOS PATH 设置（某些命令可能需要）
export PATH="/usr/sbin:/usr/bin:/bin:/sbin:$PATH"
```

### Linux

```bash
# 打开应用
uvx desktop-agent app open firefox
uvx desktop-agent app open gedit

# 常用快捷键（因桌面环境而异）
uvx desktop-agent keyboard hotkey "alt,f2"       # 运行对话框
```

---

## 七、错误恢复

### 窗口未找到

```bash
# 列出所有窗口，找到正确的标题
uvx desktop-agent app list

# 使用正确的窗口标题
uvx desktop-agent app focus "Google Chrome - My Page"
```

### 图像未找到

```bash
# 降低置信度
uvx desktop-agent screen locate button.png --confidence 0.7

# 截取当前状态分析
uvx desktop-agent screen screenshot current.png --active
```

### 点击似乎偏离

```bash
# 验证坐标在屏幕内
uvx desktop-agent screen size
uvx desktop-agent screen on-screen 1500 900

# 先移动验证位置
uvx desktop-agent mouse move 1500 900
uvx desktop-agent mouse click
```

### macOS: 权限问题

如果 Midscene 截图失败：
1. 打开 **系统设置 > 隐私与安全性 > 辅助功能**
2. 添加终端应用并启用
3. 重启终端

### macOS: Xcode 命令行工具

```bash
xcode-select --install
```

---

## 八、JSON 输出格式

所有精确控制引擎命令返回结构化 JSON：

```json
{
  "success": true,
  "command": "category.command",
  "timestamp": "2026-01-31T10:00:00Z",
  "duration_ms": 150,
  "data": { ... },
  "error": null
}
```

**错误响应：**

```json
{
  "success": false,
  "error": {
    "code": "image_not_found",
    "message": "Image file 'button.png' not found",
    "recoverable": true
  }
}
```

**错误码：**

| 错误码 | 说明 |
|--------|------|
| `invalid_argument` | 参数无效 |
| `coordinates_out_of_bounds` | 坐标超出屏幕 |
| `image_not_found` | 图像文件未找到或屏幕上未找到 |
| `window_not_found` | 目标窗口未找到 |
| `ocr_failed` | OCR 操作失败 |
| `application_not_found` | 应用未找到 |
| `permission_denied` | 权限被拒绝 |
| `timeout` | 操作超时 |

---

## 九、安全注意事项

1. **验证坐标** — 使用 `screen size` 和 `on-screen` 确认坐标有效
2. **添加延迟** — 在命令间插入适当延迟，等待 UI 响应
3. **验证图像** — 使用 `locate` 前确保图像文件存在
4. **处理失败** — 窗口变化或元素移动可能导致命令失败
5. **用户确认** — 破坏性操作前用 `message confirm` 确认

---

## 十、获取帮助

```bash
# 精确控制引擎
uvx desktop-agent --help
uvx desktop-agent mouse --help
uvx desktop-agent keyboard --help
uvx desktop-agent screen --help

# 智能视觉引擎
npx @midscene/computer@1 --help
```

---

## 技术来源

本技能融合两大桌面自动化能力：
- **PyAutoGUI 精确控制引擎** - 坐标定位、图像识别、键盘操作
- **Midscene AI 视觉引擎** - 自然语言控制、智能交互

参考文档：
- PyAutoGUI: https://pyautogui.readthedocs.io/
- Midscene: https://midscenejs.com/