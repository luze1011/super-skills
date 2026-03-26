# 🚀 Super Skills Collection

> **11 个超级技能合集** - OpenClaw 一站式能力平台

---

## ✨ 技能列表

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| 🌐 **super-browser** | AI视觉+Playwright+DevTools 浏览器自动化 | `npx skills add luze1011/super-skills@super-browser` |
| 🖥️ **desktop-control-plus** | PyAutoGUI+Midscene 桌面自动化 | `npx skills add luze1011/super-skills@desktop-control-plus` |
| 🧪 **super-testing** | pytest+Playwright+E2E 测试全流程 | `npx skills add luze1011/super-skills@super-testing` |
| 💻 **super-code** | 代码审查+Git+GitHub CLI | `npx skills add luze1011/super-skills@super-code` |
| 📄 **super-document** | PDF+Word+Excel+PPTX 文档处理 | `npx skills add luze1011/super-skills@super-document` |
| 🔍 **super-search** | 多引擎+新闻+社交搜索 | `npx skills add luze1011/super-skills@super-search` |
| ✍️ **super-writing-assistant** | 规划→撰写→润色 写作助手 | `npx skills add luze1011/super-skills@super-writing-assistant` |
| 💡 **creative-generator** | 四层能力创意生成器 | `npx skills add luze1011/super-skills@creative-generator` |
| 📢 **marketing-suite** | 策略→内容→运营 营销套件 | `npx skills add luze1011/super-skills@marketing-suite` |
| 👀 **code-review-suite** | 请求→反馈→重构 代码审查 | `npx skills add luze1011/super-skills@code-review-suite` |
| 🧪 **testing-expert** | pytest+Playwright 测试专家 | `npx skills add luze1011/super-skills@testing-expert` |

---

## 📦 一键安装全部

```bash
# 安装所有超级技能
npx skills add luze1011/super-skills --yes --global
```

---

## 🎯 快速开始

### 浏览器自动化
```bash
npx @midscene/web@1 connect --url "https://github.com"
npx @midscene/web@1 act --prompt "搜索 OpenClaw"
```

### 桌面控制
```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 act --prompt "打开记事本"
```

### 文档处理
```python
# Python 示例
from docx import Document
doc = Document()
doc.add_heading('Hello World', 0)
doc.save('demo.docx')
```

---

## 📚 技能详情

### 🌐 super-browser
融合 AI 视觉控制、Playwright 精确自动化、DevTools 调试分析、网页剪藏。

### 🖥️ desktop-control-plus
PyAutoGUI 精确坐标控制 + Midscene AI 视觉理解双引擎。

### 🧪 super-testing
Python pytest + Playwright + Vitest + Midscene E2E 测试全栈方案。

### 💻 super-code
代码审查流程 + Git 工作流 + GitHub CLI + 重构指南。

### 📄 super-document
PDF/Word/Excel/PowerPoint 文档处理全流程。

### 🔍 super-search
多搜索引擎 + AI 增强 + 新闻聚合 + 社交研究。

---

## 🔧 环境配置

部分技能需要配置环境变量：

```bash
# Midscene (浏览器/桌面自动化)
MIDSCENE_MODEL_API_KEY=your-api-key
MIDSCENE_MODEL_NAME=qwen3.5-plus
MIDSCENE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MIDSCENE_MODEL_FAMILY=qwen3.5
```

---

## 📁 目录结构

```
super-skills/
├── skills/
│   ├── super-browser/
│   ├── super-testing/
│   ├── super-code/
│   ├── super-document/
│   ├── super-search/
│   ├── super-writing-assistant/
│   ├── desktop-control-plus/
│   ├── testing-expert/
│   ├── code-review-suite/
│   ├── creative-generator/
│   └── marketing-suite/
├── README.md
└── LICENSE
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

MIT

---

_Created by 太子 (OpenClaw Agent)_