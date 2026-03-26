# Git 工作流完整指南

## 📋 目录

1. [分支策略](#分支策略)
2. [Commit 规范](#commit-规范)
3. [工作流程](#工作流程)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)

---

## 分支策略

### Git Flow 模型

最常用的分支模型，适合有计划发布周期的项目。

```
master (main)     ──●────●────●────●──  生产环境
                    \         /
develop    ──●──●──●──●──●──●──●──●──  开发环境
              \       /   \
feature/a     ●──●──●     \          功能分支
                           \
feature/b                   ●──●──●  功能分支
                  /
release     ●──●──●                    发布分支
              \
hotfix       ●──●──●                   热修复分支
```

#### 主要分支

| 分支 | 说明 | 来源 | 合并目标 |
|------|------|------|---------|
| `main/master` | 生产环境代码 | - | - |
| `develop` | 开发环境代码 | main | main (发布时) |
| `feature/*` | 新功能开发 | develop | develop |
| `release/*` | 发布准备 | develop | main + develop |
| `hotfix/*` | 紧急修复 | main | main + develop |

#### 分支命名规范

```
feature/user-authentication    # 新功能
feature/shopping-cart          # 新功能

bugfix/login-error             # Bug修复
bugfix/payment-timeout         # Bug修复

hotfix/security-vulnerability  # 紧急修复
hotfix/data-loss               # 紧急修复

release/v1.0.0                 # 发布分支
release/v2.1.0                 # 发布分支
```

---

### GitHub Flow 模型

更简单的工作流，适合持续部署的项目。

```
main  ──●────●────●────●────●──  始终可部署
         \              /
feature   ●──●──●──●──●          功能分支
```

**特点**：
- 只有一个长期分支 `main`
- 所有功能从 `main` 创建分支
- 完成后通过 PR 合并回 `main`
- 合并后立即部署

---

### GitLab Flow 模型

结合了 Git Flow 和 GitHub Flow 的优点。

```
production ──●────●────●──  生产环境
              ↑
staging    ──●────●────●──  预发布环境
              ↑
main       ──●────●────●──  开发环境
```

---

## Commit 规范

### Conventional Commits

**格式**: `<type>(<scope>): <subject>`

#### 类型 (Type)

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat(auth): add OAuth login |
| `fix` | Bug修复 | fix(api): resolve timeout issue |
| `docs` | 文档 | docs: update README |
| `style` | 格式 | style: fix indentation |
| `refactor` | 重构 | refactor: simplify auth logic |
| `test` | 测试 | test: add unit tests for auth |
| `chore` | 构建/工具 | chore: update dependencies |
| `perf` | 性能 | perf: optimize query speed |
| `ci` | CI配置 | ci: add GitHub Actions |
| `revert` | 回滚 | revert: revert previous commit |

#### 范围 (Scope)

可选，用于说明影响范围。

```
feat(auth): add JWT support
fix(api): resolve timeout issue
docs(readme): update installation guide
```

#### 主题 (Subject)

- 使用祈使句（add 而非 added）
- 首字母小写
- 结尾不加句号
- 限制在 50 字符内

#### 正文 (Body)

可选，用于详细说明：

```
feat(auth): add JWT authentication

- Implement JWT token generation
- Add token validation middleware
- Update user login flow

Closes #123
```

#### 示例

```bash
# 好的提交
git commit -m "feat(auth): implement OAuth 2.0 login"
git commit -m "fix(api): resolve race condition in request handler"
git commit -m "docs: add API documentation"

# 不好的提交
git commit -m "fix bug"
git commit -m "update code"
git commit -m "changes"
```

---

## 工作流程

### 1. 开始新功能

```bash
# 确保在最新的 develop 上
git checkout develop
git pull origin develop

# 创建功能分支
git checkout -b feature/user-profile

# 开发...
git add .
git commit -m "feat(profile): add user profile page"

# 推送到远程
git push -u origin feature/user-profile
```

### 2. 创建 Pull Request

```bash
# 使用脚本
./scripts/pr-create.sh feature/user-profile "feat: 实现用户资料页"

# 或手动
gh pr create \
  --base develop \
  --title "feat: 实现用户资料页" \
  --body "描述..."
```

### 3. 代码审查后合并

```bash
# 本地测试
git checkout develop
git pull origin develop
git merge feature/user-profile

# 或通过 GitHub/GitLab UI 合并

# 删除功能分支
git branch -d feature/user-profile
git push origin --delete feature/user-profile
```

### 4. 发布流程

```bash
# 创建发布分支
git checkout -b release/v1.0.0 develop

# 版本号更新、文档更新...
git commit -m "chore: bump version to 1.0.0"

# 合并到 main
git checkout main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# 合并回 develop
git checkout develop
git merge --no-ff release/v1.0.0

# 推送
git push origin main --tags
git push origin develop

# 删除发布分支
git branch -d release/v1.0.0
```

### 5. 热修复流程

```bash
# 从 main 创建分支
git checkout -b hotfix/security-fix main

# 修复问题
git commit -m "fix: patch security vulnerability"

# 合并到 main
git checkout main
git merge --no-ff hotfix/security-fix
git tag -a v1.0.1 -m "Hotfix: security patch"

# 合并到 develop
git checkout develop
git merge --no-ff hotfix/security-fix

# 推送
git push origin main --tags
git push origin develop
```

---

## 最佳实践

### 提交相关

✅ **推荐做法**：
- 提交要小而专注
- 一个提交只做一件事
- 写清晰的提交信息
- 提交前测试代码

❌ **避免**：
- 巨大的提交
- 模糊的提交信息
- 提交半成品
- 提交生成的文件

### 分支相关

✅ **推荐做法**：
- 保持分支短暂
- 及时合并/删除
- 遵循命名规范
- 定期同步主分支

❌ **避免**：
- 长期存在的分支
- 分支混乱
- 忘记同步更新

### 合并相关

✅ **推荐做法**：
- 使用 PR 进行代码审查
- 合并前解决冲突
- 保持提交历史清晰

❌ **避免**：
- 直接推送到主分支
- 强制推送到共享分支
- 忽略冲突直接合并

---

## 常见问题

### 1. 如何撤销最近的提交？

```bash
# 撤销提交但保留更改
git reset --soft HEAD~1

# 撤销提交并丢弃更改
git reset --hard HEAD~1

# 已推送的提交，创建反向提交
git revert <commit-hash>
```

### 2. 如何修改最后一次提交？

```bash
# 修改提交信息
git commit --amend

# 添加遗漏的文件
git add forgotten-file
git commit --amend --no-edit
```

### 3. 如何解决合并冲突？

```bash
# 查看冲突文件
git status

# 手动编辑冲突文件，然后
git add <resolved-file>
git commit

# 或使用合并工具
git mergetool
```

### 4. 如何暂存当前工作？

```bash
# 暂存
git stash

# 暂存并命名
git stash save "work in progress"

# 查看暂存列表
git stash list

# 恢复暂存
git stash pop

# 恢复指定暂存
git stash apply stash@{0}
```

### 5. 如何同步fork的仓库？

```bash
# 添加上游仓库
git remote add upstream https://github.com/original/repo.git

# 获取上游更新
git fetch upstream

# 合并到本地
git checkout main
git merge upstream/main

# 推送到自己的fork
git push origin main
```

---

## Git 命令速查

### 基础命令

```bash
git init                    # 初始化仓库
git clone <url>             # 克隆仓库
git status                  # 查看状态
git add <file>              # 添加到暂存区
git commit -m "message"     # 提交
git push                    # 推送到远程
git pull                    # 拉取更新
```

### 分支操作

```bash
git branch                  # 列出分支
git branch <name>           # 创建分支
git checkout <branch>       # 切换分支
git checkout -b <branch>    # 创建并切换
git merge <branch>          # 合并分支
git branch -d <branch>      # 删除分支
```

### 远程操作

```bash
git remote -v               # 查看远程仓库
git remote add <name> <url> # 添加远程仓库
git fetch <remote>          # 获取更新
git push <remote> <branch>  # 推送分支
git pull <remote> <branch>  # 拉取并合并
```

### 历史查看

```bash
git log                     # 查看历史
git log --oneline           # 简洁历史
git log --graph             # 图形化历史
git diff                    # 查看差异
git show <commit>           # 查看提交详情
```

---

**推荐工具**：
- Git GUI: GitKraken, Sourcetree
- CLI 增强: tig, lazygit
- Hook 管理: Husky, pre-commit