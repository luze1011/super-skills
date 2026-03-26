#!/bin/bash
# pr-create.sh - 创建标准化的 Pull Request
# 用法: ./pr-create.sh <branch-name> <title>

set -e

# 参数检查
if [ $# -lt 2 ]; then
    echo "用法: $0 <branch-name> <title>"
    echo ""
    echo "示例:"
    echo "  $0 feature/user-auth 'feat: 实现用户认证功能'"
    echo "  $0 bugfix/login-error 'fix: 修复登录失败问题'"
    exit 1
fi

BRANCH_NAME="$1"
PR_TITLE="$2"

echo "🚀 正在创建 Pull Request..."
echo ""

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 检查 gh CLI 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ 错误：未安装 GitHub CLI (gh)"
    echo "💡 请先安装: https://cli.github.com/"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 错误：未登录 GitHub CLI"
    echo "💡 请先登录: gh auth login"
    exit 1
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)

# 如果提供了分支名，检查是否需要切换
if [ -n "$BRANCH_NAME" ] && [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
    echo "⚠️  当前分支: $CURRENT_BRANCH"
    echo "目标分支: $BRANCH_NAME"
    read -p "是否切换到分支 $BRANCH_NAME? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout "$BRANCH_NAME" || {
            echo "❌ 切换分支失败"
            exit 1
        }
    fi
fi

# 获取目标分支（默认为 main 或 master）
BASE_BRANCH="main"
if ! git show-ref --verify --quiet "refs/remotes/origin/$BASE_BRANCH"; then
    BASE_BRANCH="master"
fi

echo "📋 PR 信息:"
echo "  源分支: $(git branch --show-current)"
echo "  目标分支: $BASE_BRANCH"
echo "  标题: $PR_TITLE"
echo ""

# 检查是否有未提交的变更
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  警告：有未提交的变更"
    git status -s
    echo ""
    read -p "是否继续创建 PR? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "ℹ️  已取消"
        exit 0
    fi
fi

# 检查是否已推送到远程
LOCAL_BRANCH=$(git branch --show-current)
if ! git show-ref --verify --quiet "refs/remotes/origin/$LOCAL_BRANCH"; then
    echo "⚠️  分支尚未推送到远程"
    read -p "是否推送分支到远程? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin "$LOCAL_BRANCH"
        echo "✅ 分支已推送"
    else
        echo "❌ 无法创建 PR：分支未推送到远程"
        exit 1
    fi
fi

# 生成 PR 描述
generate_pr_body() {
    local title="$1"
    local branch="$2"
    local base="$3"
    
    # 获取变更统计
    local stats=$(git diff "$base...$branch" --stat 2>/dev/null | tail -1 || echo "")
    
    # 获取变更文件列表
    local files=$(git diff "$base...$branch" --name-only 2>/dev/null || echo "")
    
    # 获取最近的 commits
    local commits=$(git log "$base..$branch" --oneline 2>/dev/null || echo "")
    
    cat <<EOF
## 📝 变更概述

$title

## 🔄 变更类型

- [ ] ✨ 新功能 (feat)
- [ ] 🐛 Bug修复 (fix)
- [ ] 📚 文档更新 (docs)
- [ ] 💄 代码格式 (style)
- [ ] ♻️ 代码重构 (refactor)
- [ ] ✅ 测试相关 (test)
- [ ] 🔧 配置变更 (chore)

## 📋 变更内容

### 修改的文件
\`\`\`
$files
\`\`\`

### 变更统计
\`\`\`
$stats
\`\`\`

### 提交历史
\`\`\`
$commits
\`\`\`

## ✅ 测试清单

- [ ] 单元测试已通过
- [ ] 集成测试已通过
- [ ] 手动测试已完成
- [ ] 代码已审查

## 📸 截图（如有）

<!-- 在这里添加截图 -->

## 🔗 相关链接

- 相关 Issue: #
- 设计文档: 

## ⚠️ 注意事项

<!-- 需要特别注意的地方 -->

---

## 📌 检查清单

提交前请确认：

- [ ] 代码符合团队规范
- [ ] 已添加必要的测试
- [ ] 文档已更新
- [ ] 无明显性能问题
- [ ] 无安全隐患
EOF
}

echo "📝 正在生成 PR 描述..."
PR_BODY=$(generate_pr_body "$PR_TITLE" "$LOCAL_BRANCH" "$BASE_BRANCH")

# 将 PR body 保存到临时文件
TEMP_FILE=$(mktemp)
echo "$PR_BODY" > "$TEMP_FILE"

echo ""
echo "📄 PR 描述已生成，正在打开编辑器..."
echo ""

# 使用 gh 创建 PR 并打开编辑器
gh pr create \
    --base "$BASE_BRANCH" \
    --title "$PR_TITLE" \
    --body-file "$TEMP_FILE" \
    --web

# 清理临时文件
rm "$TEMP_FILE"

echo ""
echo "✅ PR 创建流程已完成"