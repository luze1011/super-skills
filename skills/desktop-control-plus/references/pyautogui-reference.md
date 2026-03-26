# PyAutoGUI 精确控制引擎参考文档

本文档提供 PyAutoGUI（通过 `uvx desktop-agent`）的完整命令参考。

## 命令结构

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

## 一、鼠标控制

### mouse move

移动鼠标到指定坐标。

```bash
uvx desktop-agent mouse move <x> <y> [--duration SECONDS]
```

**参数：**
- `x` - X 坐标
- `y` - Y 坐标
- `--duration` - 移动持续时间（秒），默认 0.3

**示例：**
```bash
# 移动到屏幕中心（1920x1080）
uvx desktop-agent mouse move 960 540 --duration 0.5

# 快速移动
uvx desktop-agent mouse move 100 200
```

---

### mouse click

点击鼠标。

```bash
uvx desktop-agent mouse click [x] [y] [--button left|right|middle] [--clicks N]
```

**参数：**
- `x`, `y` - 可选，点击位置。不提供则点击当前位置
- `--button` - 鼠标按钮：`left`（默认）、`right`、`middle`
- `--clicks` - 点击次数，默认 1

**示例：**
```bash
# 左键点击
uvx desktop-agent mouse click 500 300

# 右键点击
uvx desktop-agent mouse right-click 500 300

# 双击
uvx desktop-agent mouse double-click 500 300

# 三击
uvx desktop-agent mouse click 500 300 --clicks 3
```

---

### mouse drag

拖拽鼠标。

```bash
uvx desktop-agent mouse drag <x> <y> [--duration SECONDS] [--button BUTTON]
```

**参数：**
- `x`, `y` - 目标坐标
- `--duration` - 拖拽持续时间，默认 1.0
- `--button` - 鼠标按钮，默认 `left`

**示例：**
```bash
# 拖拽到指定位置
uvx desktop-agent mouse drag 800 600 --duration 0.5

# 右键拖拽
uvx desktop-agent mouse drag 800 600 --button right
```

---

### mouse scroll

滚轮滚动。

```bash
uvx desktop-agent mouse scroll <clicks> [x] [y]
```

**参数：**
- `clicks` - 滚动格数，正数向上，负数向下
- `x`, `y` - 可选，滚动位置

**示例：**
```bash
# 向下滚动 5 格
uvx desktop-agent mouse scroll -5

# 向上滚动 3 格
uvx desktop-agent mouse scroll 3
```

---

### mouse position

获取鼠标当前位置。

```bash
uvx desktop-agent mouse position
```

**输出示例：**
```json
{
  "success": true,
  "data": {"x": 960, "y": 540}
}
```

---

## 二、键盘控制

### keyboard write

输入文本。

```bash
uvx desktop-agent keyboard write "<text>" [--interval SECONDS]
```

**参数：**
- `text` - 要输入的文本
- `--interval` - 字符间延迟（秒），默认 0.05

**示例：**
```bash
# 自然延迟输入
uvx desktop-agent keyboard write "Hello World" --interval 0.05

# 快速输入
uvx desktop-agent keyboard write "Hello World" --interval 0.01
```

---

### keyboard press

按下按键。

```bash
uvx desktop-agent keyboard press <key> [--presses N] [--interval SECONDS]
```

**参数：**
- `key` - 按键名称
- `--presses` - 按下次数，默认 1
- `--interval` - 按下间隔

**常用键名：**
| 类别 | 键名 |
|------|------|
| 修饰键 | `ctrl`, `shift`, `alt`, `win` (Windows) / `command` (macOS) |
| 特殊键 | `enter`, `tab`, `esc`, `space`, `backspace`, `delete` |
| 功能键 | `f1` - `f12` |
| 方向键 | `up`, `down`, `left`, `right` |
| 编辑键 | `home`, `end`, `pageup`, `pagedown`, `insert` |

**示例：**
```bash
# 按 Enter
uvx desktop-agent keyboard press enter

# 连续按 3 次 Tab
uvx desktop-agent keyboard press tab --presses 3
```

---

### keyboard hotkey

按下组合键。

```bash
uvx desktop-agent keyboard hotkey "<key1>,<key2>,..."
```

**参数：**
- 键名用逗号分隔，按顺序按下，然后逆序释放

**常用组合键：**

| 功能 | Windows | macOS |
|------|---------|-------|
| 复制 | `ctrl,c` | `command,c` |
| 粘贴 | `ctrl,v` | `command,v` |
| 剪切 | `ctrl,x` | `command,x` |
| 全选 | `ctrl,a` | `command,a` |
| 撤销 | `ctrl,z` | `command,z` |
| 保存 | `ctrl,s` | `command,s` |
| 查找 | `ctrl,f` | `command,f` |
| 新建 | `ctrl,n` | `command,n` |
| 关闭窗口 | `alt,f4` | `command,w` |
| 切换应用 | `alt,tab` | `command,tab` |
| 任务管理器 | `ctrl,shift,esc` | - |
| Spotlight | - | `command,space` |

**示例：**
```bash
# 复制
uvx desktop-agent keyboard hotkey "ctrl,c"

# 三键组合
uvx desktop-agent keyboard hotkey "ctrl,shift,esc"
```

---

### keyboard keydown / keyup

按住/释放按键。

```bash
uvx desktop-agent keyboard keydown <key>
uvx desktop-agent keyboard keyup <key>
```

**用途：** 需要精确控制按键时机的场景

**示例：**
```bash
# 按住 Shift
uvx desktop-agent keyboard keydown shift

# 执行其他操作...

# 释放 Shift
uvx desktop-agent keyboard keyup shift
```

---

## 三、屏幕操作

### screen screenshot

截图。

```bash
uvx desktop-agent screen screenshot <filename> [options]
```

**选项：**
- `--region "x,y,width,height"` - 截取指定区域
- `--window <title>` - 截取指定窗口
- `--active` - 截取活动窗口

**示例：**
```bash
# 全屏截图
uvx desktop-agent screen screenshot fullscreen.png

# 活动窗口截图
uvx desktop-agent screen screenshot active.png --active

# 指定窗口截图
uvx desktop-agent screen screenshot chrome.png --window "Google Chrome"

# 指定区域截图
uvx desktop-agent screen screenshot region.png --region "0,0,800,600"
```

---

### screen locate

定位图像。

```bash
uvx desktop-agent screen locate <image_path> [--confidence 0.0-1.0] [--window <title>]
```

**参数：**
- `image_path` - 图像文件路径
- `--confidence` - 匹配置信度，默认 0.9
- `--window` - 限定在指定窗口内搜索

**输出：**
```json
{
  "success": true,
  "data": {
    "found": true,
    "left": 100,
    "top": 200,
    "width": 50,
    "height": 30
  }
}
```

**示例：**
```bash
# 定位按钮
uvx desktop-agent screen locate button.png --confidence 0.8

# 在记事本中定位
uvx desktop-agent screen locate button.png --window "Notepad"
```

---

### screen locate-center

定位图像中心点。

```bash
uvx desktop-agent screen locate-center <image_path> [--confidence 0.0-1.0]
```

**输出：**
```json
{
  "success": true,
  "data": {
    "found": true,
    "x": 125,
    "y": 215
  }
}
```

**示例：**
```bash
# 定位并点击
uvx desktop-agent screen locate-center button.png
# 使用返回的坐标点击
uvx desktop-agent mouse click 125 215
```

---

### screen locate-text-coordinates

OCR 文字定位。

```bash
uvx desktop-agent screen locate-text-coordinates <text> [--window <title>] [--active]
```

**参数：**
- `text` - 要定位的文字
- `--window` - 限定窗口
- `--active` - 限定活动窗口

**示例：**
```bash
# 定位"保存"按钮
uvx desktop-agent screen locate-text-coordinates "保存" --active

# 定位并点击
uvx desktop-agent screen locate-text-coordinates "确定" --active
# 使用返回坐标点击
```

---

### screen read-all-text

读取屏幕所有文字。

```bash
uvx desktop-agent screen read-all-text [--window <title>] [--active]
```

**示例：**
```bash
# 读取活动窗口所有文字
uvx desktop-agent screen read-all-text --active

# 读取指定窗口文字
uvx desktop-agent screen read-all-text --window "Notepad"
```

---

### screen pixel

获取像素颜色。

```bash
uvx desktop-agent screen pixel <x> <y>
```

**输出：**
```json
{
  "success": true,
  "data": {
    "x": 100,
    "y": 200,
    "rgb": [255, 0, 0]
  }
}
```

---

### screen size

获取屏幕尺寸。

```bash
uvx desktop-agent screen size
```

**输出：**
```json
{
  "success": true,
  "data": {
    "width": 1920,
    "height": 1080
  }
}
```

---

### screen on-screen

验证坐标是否在屏幕内。

```bash
uvx desktop-agent screen on-screen <x> <y>
```

**输出：**
```json
{
  "success": true,
  "data": {
    "onScreen": true
  }
}
```

---

## 四、应用程序控制

### app open

打开应用程序。

```bash
uvx desktop-agent app open <name> [--arg ARGS...]
```

**参数：**
- `name` - 应用名称或路径
- `--arg` - 启动参数

**示例：**
```bash
# Windows
uvx desktop-agent app open notepad
uvx desktop-agent app open calc
uvx desktop-agent app open mspaint
uvx desktop-agent app open "chrome" --arg "https://google.com"

# macOS
uvx desktop-agent app open "Safari"
uvx desktop-agent app open "TextEdit"

# Linux
uvx desktop-agent app open firefox
uvx desktop-agent app open gedit
```

---

### app focus

聚焦窗口。

```bash
uvx desktop-agent app focus <name>
```

**参数：**
- `name` - 窗口标题（支持模糊匹配）

**示例：**
```bash
uvx desktop-agent app focus "Notepad"
uvx desktop-agent app focus "Google Chrome"
```

---

### app list

列出所有窗口。

```bash
uvx desktop-agent app list
```

**输出示例：**
```json
{
  "success": true,
  "data": {
    "windows": [
      {"title": "Notepad", "active": true},
      {"title": "Google Chrome", "active": false}
    ]
  }
}
```

---

## 五、用户对话框

### message alert

警告框。

```bash
uvx desktop-agent message alert "<text>" [--title TITLE]
```

**示例：**
```bash
uvx desktop-agent message alert "操作完成" --title "提示"
```

---

### message confirm

确认框。

```bash
uvx desktop-agent message confirm "<text>" [--title TITLE] [--buttons "OK,Cancel"]
```

**示例：**
```bash
uvx desktop-agent message confirm "确定要删除吗？" --title "确认" --buttons "是,否"
```

---

### message prompt

输入框。

```bash
uvx desktop-agent message prompt "<text>" [--title TITLE] [--default TEXT]
```

**示例：**
```bash
uvx desktop-agent message prompt "请输入文件名：" --title "保存" --default "untitled"
```

---

### message password

密码框。

```bash
uvx desktop-agent message password "<text>" [--title TITLE]
```

**示例：**
```bash
uvx desktop-agent message password "请输入密码：" --title "登录"
```

---

## 六、错误处理

所有命令返回结构化 JSON：

**成功响应：**
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
    "message": "Image not found on screen",
    "recoverable": true
  }
}
```

**错误码：**

| 错误码 | 说明 | 恢复建议 |
|--------|------|---------|
| `invalid_argument` | 参数无效 | 检查参数格式 |
| `coordinates_out_of_bounds` | 坐标超出屏幕 | 使用 `screen size` 验证 |
| `image_not_found` | 图像未找到 | 降低置信度或更新图像 |
| `window_not_found` | 窗口未找到 | 使用 `app list` 查看正确标题 |
| `ocr_failed` | OCR 失败 | 确保窗口可见 |
| `application_not_found` | 应用未找到 | 检查应用名称或路径 |
| `permission_denied` | 权限被拒绝 | 检查辅助功能权限 |
| `timeout` | 操作超时 | 增加等待时间 |

---

## 七、最佳实践

### 1. 添加适当延迟

```bash
# 打开应用后等待
uvx desktop-agent app open notepad
sleep 1
uvx desktop-agent keyboard write "Hello"
```

### 2. 验证坐标

```bash
# 检查坐标是否在屏幕内
uvx desktop-agent screen on-screen 1500 900
uvx desktop-agent mouse click 1500 900
```

### 3. 使用置信度调优

```bash
# 高精度定位
uvx desktop-agent screen locate button.png --confidence 0.95

# 宽松匹配
uvx desktop-agent screen locate button.png --confidence 0.7
```

### 4. 窗口操作流程

```bash
# 标准流程
uvx desktop-agent app list                    # 查看窗口
uvx desktop-agent app open notepad            # 打开应用
sleep 1                                       # 等待启动
uvx desktop-agent app focus "Notepad"         # 聚焦窗口
uvx desktop-agent screen screenshot --active  # 确认状态
```

---

## 参考链接

- PyAutoGUI 官方文档: https://pyautogui.readthedocs.io/
- PyAutoGUI GitHub: https://github.com/asweigart/pyautogui