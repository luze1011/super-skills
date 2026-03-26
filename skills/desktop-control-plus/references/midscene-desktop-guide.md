# Midscene 智能视觉引擎指南

本文档提供 Midscene Desktop 的完整使用指南。

## 概述

Midscene.js 是 **AI 驱动、视觉优先的 UI 自动化工具**：
- 🧠 用自然语言描述任务，AI 自动规划执行
- 👁️ 纯视觉定位，不依赖 DOM
- 🖥️ 支持 Web、Android、iOS、桌面全平台

**GitHub**: https://github.com/web-infra-dev/midscene  
**文档**: https://midscenejs.com  
**Stars**: 12k+

---

## 一、前置条件

### 环境变量配置

需要配置支持视觉定位的模型。**推荐 Qwen3.5 Plus**。

```powershell
# 初始化脚本
. .\skills\desktop-control-plus\scripts\init-env.ps1

# 或手动设置
$env:MIDSCENE_MODEL_API_KEY = "your-api-key"
$env:MIDSCENE_MODEL_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
$env:MIDSCENE_MODEL_NAME = "qwen3.5-plus"
$env:MIDSCENE_MODEL_FAMILY = "qwen3.5"
$env:MIDSCENE_MODEL_REASONING_ENABLED = "false"
```

### 推荐模型

| 模型 | 特点 | 推荐度 |
|------|------|--------|
| **Qwen 3.5** | 中文友好、速度快 | ⭐⭐⭐⭐⭐ |
| Doubao Seed 2.0 Lite | 阿里云、稳定 | ⭐⭐⭐⭐ |
| Zhipu GLM-4.6V | 智谱、视觉强 | ⭐⭐⭐⭐ |
| Gemini-3-Pro | Google、多模态 | ⭐⭐⭐ |

---

## 二、核心命令

### connect - 连接桌面

```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 connect --displayId <id>
```

**参数：**
- `--displayId` - 指定显示器 ID（多显示器环境）

**输出：**
```
✓ Connected to display 0 (1920x1080)
```

---

### disconnect - 断开连接

```bash
npx @midscene/computer@1 disconnect
```

**重要：** 任务完成后务必断开连接，释放资源。

---

### take_screenshot - 截图

```bash
npx @midscene/computer@1 take_screenshot
```

**输出：** 截图保存路径

**用途：**
- 验证当前状态
- 调试操作结果
- 获取 AI 分析依据

---

### act - 执行动作

这是 **核心命令**，用自然语言描述想要完成的任务。

```bash
npx @midscene/computer@1 act --prompt "你的指令"
npx @midscene/computer@1 act --prompt "你的指令" --deepThink
```

**参数：**
- `--prompt` - 自然语言指令（必填）
- `--deepThink` - 启用深度思考模式（复杂任务）

**执行时间：** 典型命令需要约 1 分钟，复杂任务可能更久

---

### list_displays - 列出显示器

```bash
npx @midscene/computer@1 list_displays
```

**输出：**
```
Display 0: 1920x1080 (Primary)
Display 1: 2560x1440
```

---

## 三、提示词技巧

### 好的提示词

```bash
# ✅ 清晰具体
"打开记事本，输入 Hello World，保存到桌面，文件名 test.txt"
"在 Chrome 中搜索 Midscene GitHub，打开第一个结果"
"打开设置，找到关于本机，查看系统版本"

# ✅ 包含验证条件
"填写注册表单，确保所有字段通过验证，但不要真正提交"

# ✅ 合并相关操作
"打开 Word，新建文档，输入标题，保存到桌面"
```

### 不好的提示词

```bash
# ❌ 太模糊
"搜索一下"
"帮我做这个"

# ❌ 缺少关键信息
"打开那个应用"  # 哪个应用？
"输入一些文字"  # 输入什么？

# ❌ 过于复杂，应拆分
"打开 Word，写一篇文章，格式化，插入图片，导出 PDF，发送邮件"
```

### 提示词模板

#### 应用操作
```
"打开 <应用名>，<具体操作>"
```

#### 表单填写
```
"在 <表单名> 中填写：<字段1>：<值1>，<字段2>：<值2>"
```

#### 搜索任务
```
"在 <应用> 中搜索 <关键词>，<后续操作>"
```

#### 数据提取
```
"从 <界面> 中提取 <信息>，返回结果"
```

---

## 四、deepThink 模式

复杂任务启用深度思考，提高成功率。

### 何时使用

- 多步骤任务（>3 步）
- 需要决策的任务
- 复杂 UI 交互
- 首次尝试失败后

### 示例

```bash
# 复杂表单填写
npx @midscene/computer@1 act --prompt "完成 GitHub 注册表单，确保所有字段通过验证" --deepThink

# 多步骤操作
npx @midscene/computer@1 act --prompt "登录电商网站，搜索商品，加入购物车" --deepThink

# 需要理解的任务
npx @midscene/computer@1 act --prompt "找到最新的 PDF 文件并发送给张三" --deepThink
```

### 支持的模型

`deepThink` 支持以下模型：
- qwen3.5 ✅
- qwen3-vl
- doubao-seed
- glm-v

---

## 五、执行报告

每次执行后生成可视化 HTML 报告：

```
./midscene_run/report/computer-YYYY-MM-DD_HH-MM-SS-xxx.html
```

### 报告内容

| 内容 | 说明 |
|------|------|
| 执行步骤截图 | 每步操作的截图 |
| AI 规划过程 | AI 如何理解和规划任务 |
| 执行时间统计 | 各步骤耗时 |
| 错误信息 | 如有错误，显示详情 |

### 用途

- 调试失败的操作
- 分析性能瓶颈
- 理解 AI 决策过程

---

## 六、工作流程

### 标准流程

```bash
# 1. 连接桌面
npx @midscene/computer@1 connect

# 2. 执行动作
npx @midscene/computer@1 act --prompt "你的指令"

# 3. 截图确认
npx @midscene/computer@1 take_screenshot

# 4. 断开连接
npx @midscene/computer@1 disconnect
```

### 调试流程

```bash
# 1. 连接
npx @midscene/computer@1 connect

# 2. 先截图了解当前状态
npx @midscene/computer@1 take_screenshot

# 3. 尝试简单动作
npx @midscene/computer@1 act --prompt "将鼠标移动到屏幕中央"

# 4. 再次截图确认
npx @midscene/computer@1 take_screenshot

# 5. 执行主要任务
npx @midscene/computer@1 act --prompt "你的实际任务"

# 6. 断开
npx @midscene/computer@1 disconnect
```

### 错误恢复

```bash
# 如果任务失败，尝试：
# 1. 使用 deepThink 模式
npx @midscene/computer@1 act --prompt "同样的任务" --deepThink

# 2. 拆分任务
npx @midscene/computer@1 act --prompt "第一步：打开应用"
npx @midscene/computer@1 take_screenshot
npx @midscene/computer@1 act --prompt "第二步：执行操作"

# 3. 更具体的指令
# 原来："保存文件"
# 改进："点击文件菜单，选择保存，在文件名输入框输入 test.txt，点击保存按钮"
```

---

## 七、高级用法

### 多显示器

```bash
# 列出所有显示器
npx @midscene/computer@1 list_displays

# 连接指定显示器
npx @midscene/computer@1 connect --displayId 1
```

### 条件判断

```bash
# 在提示词中包含条件
npx @midscene/computer@1 act --prompt "如果看到登录按钮，点击它；否则跳过"

# 带验证的操作
npx @midscene/computer@1 act --prompt "点击提交按钮，如果出现错误提示，截图并告诉我"
```

### 数据提取

```bash
# 提取文本
npx @midscene/computer@1 act --prompt "读取屏幕上的所有文字，告诉我有什么内容"

# 提取特定信息
npx @midscene/computer@1 act --prompt "找到价格信息，告诉我商品价格是多少"

# 表格数据
npx @midscene/computer@1 act --prompt "读取表格中的数据，以 JSON 格式返回"
```

### 循环操作

```bash
# 批量处理
npx @midscene/computer@1 act --prompt "选中所有邮件，然后删除" --deepThink

# 重复操作
npx @midscene/computer@1 act --prompt "点击下一页按钮，直到没有更多内容"
```

---

## 八、平台特定

### Windows

```bash
# Windows 特定操作
npx @midscene/computer@1 act --prompt "按 Win 键打开开始菜单"

# 任务管理器
npx @midscene/computer@1 act --prompt "打开任务管理器"

# 设置
npx @midscene/computer@1 act --prompt "打开 Windows 设置"
```

### macOS

```bash
# macOS 特定操作
npx @midscene/computer@1 act --prompt "按 Command+Space 打开 Spotlight"

# Finder
npx @midscene/computer@1 act --prompt "打开 Finder"

# 系统偏好设置
npx @midscene/computer@1 act --prompt "打开系统偏好设置"
```

### 权限设置

#### macOS

如果截图失败：
1. 打开 **系统设置 > 隐私与安全性 > 辅助功能**
2. 添加终端应用并启用
3. 重启终端

#### Windows

- 通常无需额外权限
- 如遇问题，以管理员身份运行

---

## 九、故障排除

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `model name is required` | 环境变量未设置 | 运行初始化脚本 |
| `connection failed` | 显示器连接失败 | 检查权限，重试 |
| `action timeout` | 任务超时 | 拆分任务或启用 deepThink |
| `element not found` | UI 元素未找到 | 更具体的描述 |

### 调试技巧

1. **先截图再操作**
   ```bash
   npx @midscene/computer@1 connect
   npx @midscene/computer@1 take_screenshot
   # 分析截图后再执行
   ```

2. **使用 deepThink**
   ```bash
   # 首次尝试不加 deepThink
   npx @midscene/computer@1 act --prompt "任务"
   # 失败后加 deepThink
   npx @midscene/computer@1 act --prompt "任务" --deepThink
   ```

3. **查看报告**
   ```bash
   # 打开最新报告
   # 报告在 ./midscene_run/report/ 目录
   ```

---

## 十、最佳实践

### 1. 一个 act 完成相关操作

```bash
# ✅ 好
npx @midscene/computer@1 act --prompt "打开记事本，输入 Hello，保存到桌面"

# ❌ 不好（分成多个 act）
npx @midscene/computer@1 act --prompt "打开记事本"
npx @midscene/computer@1 act --prompt "输入 Hello"
npx @midscene/computer@1 act --prompt "保存"
```

### 2. 明确目标而非步骤

```bash
# ✅ 目标导向
npx @midscene/computer@1 act --prompt "在 Chrome 中搜索 Python 教程"

# ❌ 过于细节
npx @midscene/computer@1 act --prompt "点击 Chrome 图标，等待打开，点击地址栏，输入 google.com..."
```

### 3. 包含验证条件

```bash
# ✅ 包含验证
npx @midscene/computer@1 act --prompt "填写表单并确保所有字段通过验证"

# ❌ 无验证
npx @midscene/computer@1 act --prompt "填写表单"
```

### 4. 处理异常情况

```bash
# 包含异常处理
npx @midscene/computer@1 act --prompt "点击保存按钮，如果出现错误提示，告诉我错误内容"
```

---

## 参考链接

- Midscene 官方文档: https://midscenejs.com/
- Midscene GitHub: https://github.com/web-infra-dev/midscene
- Midscene Discord: https://discord.gg/midscene