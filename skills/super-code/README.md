# Super Code - 超级代码技能

一个综合性的代码辅助技能，提供代码审查、Git工作流、GitHub CLI操作和重构模式指导。

## 🎯 功能特点

### 1. 代码审查
- 自动检测代码问题
- 提供改进建议
- 检查安全漏洞
- 评估代码质量

### 2. Git 工作流
- 分支管理策略
- Commit 规范指导
- 工作流程指南

### 3. GitHub CLI 操作
- PR 创建和管理
- Issue 处理
- 自动化脚本

### 4. 重构模式
- 代码坏味道识别
- 重构技巧指导
- 性能优化建议

## 📁 目录结构

```
super-code/
├── SKILL.md                    # 主技能文件
├── scripts/                    # 自动化脚本
│   ├── git-commit-gen.sh       # 自动生成 commit message
│   ├── pr-create.sh            # 创建标准化 PR
│   └── code-review.sh          # 执行代码审查
├── references/                 # 参考文档
│   ├── git-workflow.md         # Git 工作流完整指南
│   ├── github-cli-guide.md     # GitHub CLI 完整命令参考
│   └── refactor-patterns.md    # 重构模式大全
└── assets/                     # 模板资源
    ├── commit-template.txt     # Commit message 模板
    └── pr-template.md          # PR 描述模板
```

## 🚀 快速开始

### 使用脚本

```bash
# 代码审查
./scripts/code-review.sh src/auth.js

# 生成 commit message
./scripts/git-commit-gen.sh

# 创建 PR
./scripts/pr-create.sh feature/user-auth "feat: 实现用户认证"
```

### 查看文档

- **Git 工作流**: `references/git-workflow.md`
- **GitHub CLI**: `references/github-cli-guide.md`
- **重构模式**: `references/refactor-patterns.md`

### 使用模板

- **Commit 模板**: `assets/commit-template.txt`
- **PR 模板**: `assets/pr-template.md`

## 📖 详细说明

请阅读 `SKILL.md` 获取完整的使用指南和最佳实践。

---

**创建时间**: 2026-03-26  
**版本**: 1.0.0  
**作者**: OpenClaw Assistant