---
name: super-code
description: Comprehensive coding assistant for code review, Git workflows, GitHub CLI operations, and refactoring patterns. Use this skill whenever the user mentions code review, git operations, creating PRs, refactoring, commit messages, branch management, or any code quality improvement task.
---

# Super Code - 代码审查与工作流技能

一个综合性的代码辅助技能，提供代码审查、Git工作流、GitHub CLI操作和重构模式指导。

## 🎯 核心能力

### 1. 代码审查 (Code Review)
- 自动检测代码问题
- 提供改进建议
- 检查安全漏洞
- 评估代码质量

### 2. Git 工作流 (Git Workflow)
- 分支管理策略
- Commit 规范
- Merge/Rebase 选择
- 冲突解决

### 3. GitHub CLI 操作
- PR 创建和管理
- Issue 处理
- Repository 管理
- 自动化工作流

### 4. 重构模式 (Refactoring Patterns)
- 代码坏味道识别
- 重构技巧
- 性能优化
- 架构改进

---

## 📋 使用指南

### 代码审查流程

**何时使用**：当你需要审查代码、发现潜在问题或改进代码质量时。

**审查清单**：
1. **代码风格** - 是否符合团队规范？
2. **命名规范** - 变量/函数名是否清晰？
3. **代码复杂度** - 是否有过度复杂的逻辑？
4. **潜在Bug** - 是否有边界条件未处理？
5. **性能问题** - 是否有性能瓶颈？
6. **安全问题** - 是否有安全漏洞？
7. **测试覆盖** - 是否有足够的测试？

**审查命令**：
```bash
# 使用脚本进行代码审查
./scripts/code-review.sh <file-path>
```

---

### Git 工作流指南

**何时使用**：当你需要管理Git分支、提交代码或处理合并时。

#### 分支策略
```
main (生产分支)
  └── develop (开发分支)
        ├── feature/* (功能分支)
        ├── bugfix/* (修复分支)
        └── release/* (发布分支)
```

#### Commit 规范
格式：`<type>(<scope>): <subject>`

**类型说明**：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**：
```
feat(auth): add JWT authentication
fix(api): resolve timeout issue in user API
docs(readme): update installation guide
```

**自动生成 Commit Message**：
```bash
# 使用脚本自动生成规范的 commit message
./scripts/git-commit-gen.sh
```

详细工作流参考：`references/git-workflow.md`

---

### GitHub CLI 操作指南

**何时使用**：当你需要创建PR、管理Issue或进行GitHub操作时。

#### 常用命令
```bash
# 创建 PR
gh pr create --title "feat: add new feature" --body "Description..."

# 查看 PR 列表
gh pr list

# 查看 Issue
gh issue list

# 创建仓库
gh repo create <repo-name> --public
```

**自动创建 PR**：
```bash
# 使用脚本创建标准化的 PR
./scripts/pr-create.sh <branch-name> <title>
```

详细指南参考：`references/github-cli-guide.md`

---

### 重构模式指南

**何时使用**：当你发现代码坏味道或需要改进代码结构时。

#### 常见代码坏味道
1. **重复代码** - 提取方法/类
2. **过长函数** - 分解函数
3. **过大类** - 提取类
4. **过长参数列表** - 引入参数对象
5. **发散式变化** - 提取类
6. **散弹式修改** - 移动方法/字段
7. **依恋情结** - 移动方法
8. **数据泥团** - 提取对象

#### 重构步骤
1. **识别问题** - 找到代码坏味道
2. **编写测试** - 确保行为不变
3. **小步重构** - 每次只改一点
4. **运行测试** - 验证正确性
5. **提交代码** - 保留历史记录

详细模式参考：`references/refactor-patterns.md`

---

## 🔧 脚本工具

本技能包含以下自动化脚本：

| 脚本 | 功能 | 使用场景 |
|------|------|---------|
| `git-commit-gen.sh` | 自动生成规范的commit message | 提交代码前 |
| `pr-create.sh` | 创建标准化的PR | 完成功能开发后 |
| `code-review.sh` | 执行代码审查 | 合并代码前 |

---

## 📚 参考文档

本技能附带以下参考文档：

| 文档 | 内容 | 何时阅读 |
|------|------|---------|
| `git-workflow.md` | Git工作流详细指南 | 需要管理分支时 |
| `github-cli-guide.md` | GitHub CLI完整命令参考 | 使用gh命令时 |
| `refactor-patterns.md` | 重构模式大全 | 改进代码结构时 |

---

## 🎨 模板资源

本技能提供以下模板：

| 模板 | 用途 | 位置 |
|------|------|------|
| `commit-template.txt` | Commit message模板 | `assets/commit-template.txt` |
| `pr-template.md` | PR描述模板 | `assets/pr-template.md` |

---

## 💡 最佳实践

### 代码审查
1. **及时审查** - PR创建后24小时内完成审查
2. **建设性反馈** - 指出问题的同时提供解决方案
3. **关注重点** - 优先关注架构、安全、性能问题
4. **保持尊重** - 对事不对人

### Git 工作流
1. **频繁提交** - 每个逻辑单元一个commit
2. **有意义的message** - 说明"为什么"而不只是"做了什么"
3. **保持分支整洁** - 及时合并/删除已完成的分支
4. **使用PR** - 所有代码变更都通过PR合并

### 重构
1. **小步前进** - 每次重构保持最小改动
2. **测试先行** - 确保有足够的测试覆盖
3. **保持功能** - 重构不改变外部行为
4. **及时提交** - 每个重构步骤都独立提交

---

## 🚀 快速开始

### 场景 1：代码审查
```
用户：帮我审查一下 src/auth.js 这个文件
```
→ 执行 `./scripts/code-review.sh src/auth.js`

### 场景 2：创建规范的commit
```
用户：我修改了用户登录功能，帮我生成commit message
```
→ 执行 `./scripts/git-commit-gen.sh`

### 场景 3：创建PR
```
用户：我完成了用户管理功能，帮我创建PR
```
→ 执行 `./scripts/pr-create.sh feature/user-management "feat: 实现用户管理功能"`

### 场景 4：重构建议
```
用户：这段代码太长了，怎么重构？
```
→ 参考 `references/refactor-patterns.md` 中的"过长函数"模式

---

## 📖 扩展阅读

需要更深入的信息时，请查阅：
- Git工作流详细说明：阅读 `references/git-workflow.md`
- GitHub CLI完整命令：阅读 `references/github-cli-guide.md`
- 重构模式详解：阅读 `references/refactor-patterns.md`

---

**记住**：好的代码是写出来的，更是改出来的。持续改进，追求卓越！