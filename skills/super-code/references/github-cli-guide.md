# GitHub CLI 完整指南

## 📋 目录

1. [安装与配置](#安装与配置)
2. [常用命令](#常用命令)
3. [PR 管理](#pr-管理)
4. [Issue 管理](#issue-管理)
5. [仓库管理](#仓库管理)
6. [高级用法](#高级用法)

---

## 安装与配置

### 安装

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install GitHub.cli
# 或
choco install gh

# 验证安装
gh --version
```

### 认证

```bash
# 登录
gh auth login

# 检查认证状态
gh auth status

# 刷新token
gh auth refresh

# 登出
gh auth logout
```

### 配置

```bash
# 设置默认编辑器
gh config set editor "code --wait"

# 设置默认浏览器
gh config set browser "chrome"

# 设置git协议
gh config set git_protocol ssh

# 查看配置
gh config list
```

---

## 常用命令

### 仓库操作

```bash
# 创建仓库
gh repo create my-project --public --clone

# 创建私有仓库
gh repo create my-project --private

# 克隆仓库
gh repo clone owner/repo

# 查看仓库信息
gh repo view owner/repo

# 在浏览器中打开
gh repo view --web

# 删除仓库（需确认）
gh repo delete owner/repo --yes

# Fork 仓库
gh repo fork owner/repo --clone

# 列出仓库
gh repo list
gh repo list owner --limit 50
```

### Gist 操作

```bash
# 创建 gist
gh gist create file.txt

# 创建私密 gist
gh gist create file.txt --private

# 查看 gist
gh gist view <gist-id>

# 编辑 gist
gh gist edit <gist-id>

# 列出 gist
gh gist list
```

---

## PR 管理

### 创建 PR

```bash
# 基础创建
gh pr create

# 指定标题和描述
gh pr create --title "feat: new feature" --body "Description..."

# 从文件读取描述
gh pr create --title "feat: new feature" --body-file pr-description.md

# 指定基础分支
gh pr create --base develop --head feature/new-feature

# 指定审查者
gh pr create --reviewer user1,user2

# 指定标签
gh pr create --label "enhancement,documentation"

# 指定指派人
gh pr create --assignee @me

# 创建草稿 PR
gh pr create --draft

# 使用模板
gh pr create --template pr-template.md
```

### 查看 PR

```bash
# 列出 PR
gh pr list

# 过滤 PR
gh pr list --state open --label bug
gh pr list --author @me
gh pr list --base main

# 查看 PR 详情
gh pr view 123

# 在浏览器中查看
gh pr view 123 --web

# 查看 PR 的 diff
gh pr diff 123

# 查看 PR 的检查状态
gh pr checks 123
```

### 管理 PR

```bash
# 检出 PR
gh pr checkout 123

# 合并 PR
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# 关闭 PR
gh pr close 123

# 重新打开 PR
gh pr reopen 123

# 准备审查
gh pr ready 123

# 转换为草稿
gh pr ready 123 --undo

# 添加审查者
gh pr edit 123 --add-reviewer user1

# 添加标签
gh pr edit 123 --add-label "bug,high-priority"
```

### PR 审查

```bash
# 查看审查状态
gh pr view 123 --json reviews

# 批准 PR
gh pr review 123 --approve

# 请求修改
gh pr review 123 --request-changes --body "需要修复..."

# 评论 PR
gh pr review 123 --comment --body "LGTM!"

# 添加单行评论
gh pr comment 123 --body "Nice work!"
```

---

## Issue 管理

### 创建 Issue

```bash
# 交互式创建
gh issue create

# 指定标题和内容
gh issue create --title "Bug in login" --body "Description..."

# 从文件读取内容
gh issue create --title "Bug" --body-file issue.md

# 指定标签
gh issue create --label "bug,high-priority"

# 指定指派人
gh issue create --assignee @me

# 指定项目
gh issue create --project "Roadmap"

# 指定里程碑
gh issue create --milestone "v1.0"
```

### 查看 Issue

```bash
# 列出 issue
gh issue list

# 过滤 issue
gh issue list --state open --label bug
gh issue list --assignee @me
gh issue list --author user1
gh issue list --milestone "v1.0"

# 查看详情
gh issue view 123

# 在浏览器中查看
gh issue view 123 --web
```

### 管理 Issue

```bash
# 关闭 issue
gh issue close 123

# 重新打开
gh issue reopen 123

# 编辑 issue
gh issue edit 123 --title "New title"
gh issue edit 123 --add-label "bug"
gh issue edit 123 --add-assignee @me

# 评论
gh issue comment 123 --body "Fixed in #456"

# 传输到另一个仓库
gh issue transfer 123 owner/repo
```

---

## 仓库管理

### Release 管理

```bash
# 创建 release
gh release create v1.0.0

# 带说明创建
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes..."

# 从文件读取说明
gh release create v1.0.0 --notes-file RELEASE.md

# 上传资源文件
gh release create v1.0.0 ./dist/app.zip

# 列出 releases
gh release list

# 查看 release
gh release view v1.0.0

# 下载 release
gh release download v1.0.0

# 删除 release
gh release delete v1.0.0 --yes
```

### Actions 管理

```bash
# 列出 workflows
gh workflow list

# 查看 workflow
gh workflow view workflow.yml

# 运行 workflow
gh workflow run workflow.yml

# 带参数运行
gh workflow run workflow.yml -f param=value

# 查看 runs
gh run list

# 查看 run 详情
gh run view 123456

# 查看 run 日志
gh run view 123456 --log

# 重新运行
gh run rerun 123456

# 取消运行
gh run cancel 123456

# 下载 artifacts
gh run download 123456
```

### Secrets 管理

```bash
# 列出 secrets
gh secret list

# 设置 secret
gh secret set API_KEY
gh secret set API_KEY --body "secret-value"

# 从文件设置
gh secret set API_KEY < secret.txt

# 删除 secret
gh secret delete API_KEY
```

### Variables 管理

```bash
# 列出 variables
gh variable list

# 设置 variable
gh variable set ENV_NAME --body "value"

# 更新 variable
gh variable set ENV_NAME --body "new-value"

# 删除 variable
gh variable delete ENV_NAME
```

---

## 高级用法

### API 调用

```bash
# GET 请求
gh api repos/owner/repo

# POST 请求
gh api repos/owner/repo/issues -f title="New issue"

# 使用 jq 处理输出
gh api repos/owner/repo --jq '.name'

# 分页查询
gh api repos/owner/repo/issues --paginate
```

### 脚本化

```bash
# 批量操作 PR
gh pr list --state open --json number --jq '.[].number' | \
  while read pr; do
    gh pr close $pr
  done

# 获取仓库统计
gh api repos/owner/repo/stats/contributors

# 批量创建 issue
cat issues.txt | while read title; do
  gh issue create --title "$title" --body ""
done
```

### 别名设置

```bash
# 创建别名
gh alias set pc 'pr create --title "$1" --body "$2"'
gh alias set pv 'pr view --web'
gh alias set il 'issue list --assignee @me'

# 使用别名
gh pc "fix: bug" "description"
gh pv
gh il

# 列出别名
gh alias list

# 删除别名
gh alias delete pc
```

### 扩展

```bash
# 安装扩展
gh extension install owner/gh-extension

# 列出扩展
gh extension list

# 升级扩展
gh extension upgrade extension-name

# 创建扩展
gh extension create my-extension
```

---

## 实用脚本

### 1. 快速创建并推送分支

```bash
#!/bin/bash
# quick-pr.sh
BRANCH=$1
TITLE=$2

git checkout -b "$BRANCH"
git push -u origin "$BRANCH"
gh pr create --title "$TITLE" --fill
```

### 2. 批量关闭 PR

```bash
#!/bin/bash
# close-stale-prs.sh
gh pr list --state open --json number,updatedAt --jq '.[] | select(.updatedAt < "2024-01-01") | .number' | \
  while read pr; do
    gh pr close $pr --comment "Closing stale PR"
  done
```

### 3. 检查所有仓库的 PR

```bash
#!/bin/bash
# check-all-prs.sh
gh repo list --json name --jq '.[].name' | \
  while read repo; do
    echo "=== $repo ==="
    gh pr list -R owner/$repo
  done
```

### 4. 自动合并通过检查的 PR

```bash
#!/bin/bash
# auto-merge.sh
gh pr list --state open --json number,mergeable --jq '.[] | select(.mergeable == "MERGEABLE") | .number' | \
  while read pr; do
    if gh pr checks $pr; then
      gh pr merge $pr --auto
    fi
  done
```

---

## 环境变量

```bash
# 设置 token
export GH_TOKEN=ghp_xxxx

# 设置企业
export GH_HOST=github.enterprise.com

# 设置默认仓库
export GH_REPO=owner/repo

# 禁用分页
export GH_NO_PAGER=1
```

---

**参考资源**：
- 官方文档: https://cli.github.com/manual/
- 手册页: `gh help`
- 指令帮助: `gh <command> --help`