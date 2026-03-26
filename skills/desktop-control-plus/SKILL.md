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

**分类：** `mouse` | `keyboard` | `screen` | `message` | `app`

### 常用命令速查

```bash
# 鼠标控制
uvx desktop-agent mouse move <x> <y> [--duration SECONDS]
uvx desktop-agent mouse click [x] [y] [--button left|right|middle]
uvx desktop-agent mouse scroll <clicks>  # 正数上，负数下

# 键盘控制
uvx desktop-agent keyboard write "<text>" [--interval SECONDS]
uvx desktop-agent keyboard hotkey "<key1>,<key2>"  # 如 "ctrl,c"
uvx desktop-agent keyboard press <key> [--presses N]

# 屏幕操作
uvx desktop-agent screen screenshot <filename> [--active]
uvx desktop-agent screen locate <image_path> [--confidence 0.8]
uvx desktop-agent screen locate-text-coordinates <text>  # OCR 定位

# 应用控制
uvx desktop-agent app open <name>
uvx desktop-agent app focus <name>
uvx desktop-agent app list
```

**详细文档：** 见 `references/pyautogui-reference.md`

---

## 二、智能视觉引擎（Midscene）

### 前置条件

```powershell
# 初始化环境变量
. .\skills\desktop-control-plus\scripts\init-env.ps1
```

### 核心命令

```bash
# 连接桌面
npx @midscene/computer@1 connect

# 截图
npx @midscene/computer@1 take_screenshot

# 执行动作（自然语言）
npx @midscene/computer@1 act --prompt "在搜索框输入 hello world 并按回车"

# 复杂任务启用深度思考
npx @midscene/computer@1 act --prompt "完成复杂操作" --deepThink

# 断开连接
npx @midscene/computer@1 disconnect
```

### 提示词技巧

**好的提示词：**
```bash
# ✅ 清晰具体，合并相关操作
"打开记事本，输入 Hello World，保存到桌面，文件名 test.txt"
"在 Chrome 中搜索 Midscene GitHub，打开第一个结果"
```

**不好的提示词：**
```bash
# ❌ 太模糊
"搜索一下"
"帮我做这个"
```

**详细文档：** 见 `references/midscene-desktop-guide.md`

---

## 三、决策指南

```
需要与桌面应用交互？
├── 精确坐标已知 → 精确控制引擎
├── 需要图像识别 → 精确控制引擎
├── 需要 OCR → 精确控制引擎
├── 需要快捷键 → 精确控制引擎
├── 复杂 UI 交互 → 智能视觉引擎
├── 目标驱动任务 → 智能视觉引擎
└── 混合需求 → 混合流程
```

---

## 四、工作流程模式

### 模式 A：精确控制流程

```bash
uvx desktop-agent screen size           # 获取屏幕尺寸
uvx desktop-agent app open notepad      # 打开应用
uvx desktop-agent keyboard write "Hello" # 输入文本
uvx desktop-agent keyboard hotkey "ctrl,s" # 快捷键保存
```

### 模式 B：智能视觉流程

```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "打开 Safari，访问 github.com"
npx @midscene/computer@1 take_screenshot
npx @midscene/computer@1 disconnect
```

### 模式 C：混合流程（推荐）

```bash
# 阶段1：精确控制打开应用
uvx desktop-agent app open "Google Chrome"

# 阶段2：智能视觉执行复杂操作
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "在 Chrome 中搜索 Python 教程"
npx @midscene/computer@1 disconnect

# 阶段3：精确控制执行快捷键
uvx desktop-agent keyboard hotkey "ctrl,s"
```

---

## 五、常用场景速查

### 场景1：打开应用并输入

```bash
uvx desktop-agent app open notepad
uvx desktop-agent keyboard write "Hello from Desktop Control Plus!"
```

### 场景2：截图与 OCR

```bash
uvx desktop-agent screen screenshot active.png --active
uvx desktop-agent screen read-all-text --active
uvx desktop-agent screen locate-text-coordinates "保存" --active
```

### 场景3：复制粘贴

```bash
uvx desktop-agent keyboard hotkey "ctrl,a"  # 全选
uvx desktop-agent keyboard hotkey "ctrl,c"  # 复制
uvx desktop-agent mouse click 500 600       # 定位
uvx desktop-agent keyboard hotkey "ctrl,v"  # 粘贴
```

### 场景4：复杂 UI 交互

```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "在 Word 中打开最近文档，复制第一段"
npx @midscene/computer@1 disconnect
```

---

## 六、平台快捷键速查

### Windows

| 操作 | 命令 |
|------|------|
| 显示桌面 | `uvx desktop-agent keyboard hotkey "win,d"` |
| 资源管理器 | `uvx desktop-agent keyboard hotkey "win,e"` |
| 切换窗口 | `uvx desktop-agent keyboard hotkey "alt,tab"` |
| 运行对话框 | `uvx desktop-agent keyboard hotkey "win,r"` |

### macOS

| 操作 | 命令 |
|------|------|
| Spotlight | `uvx desktop-agent keyboard hotkey "command,space"` |
| 应用切换 | `uvx desktop-agent keyboard hotkey "command,tab"` |
| 退出应用 | `uvx desktop-agent keyboard hotkey "command,q"` |
| 截图 | `uvx desktop-agent keyboard hotkey "command,shift,3"` |

---

## 七、错误恢复

| 问题 | 解决方案 |
|------|---------|
| 窗口未找到 | `uvx desktop-agent app list` 查看正确标题 |
| 图像未找到 | 降低置信度 `--confidence 0.7` |
| 点击偏离 | 验证坐标 `uvx desktop-agent screen on-screen <x> <y>` |
| macOS 权限 | 系统设置 > 隐私与安全性 > 辅助功能 |

---

## 八、获取帮助

```bash
# 精确控制引擎
uvx desktop-agent --help

# 智能视觉引擎
npx @midscene/computer@1 --help
```

---

## 技术来源

- **PyAutoGUI 精确控制引擎** - 坐标定位、图像识别、键盘操作
- **Midscene AI 视觉引擎** - 自然语言控制、智能交互

参考文档：
- PyAutoGUI: https://pyautogui.readthedocs.io/
- Midscene: https://midscenejs.com/