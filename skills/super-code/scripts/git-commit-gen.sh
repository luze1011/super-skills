#!/bin/bash
# git-commit-gen.sh - 自动生成规范的 Git Commit Message
# 用法: ./git-commit-gen.sh

set -e

echo "🔍 正在分析 Git 变更..."

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 获取变更统计
STAGED_FILES=$(git diff --cached --name-only)
UNSTAGED_FILES=$(git diff --name-only)
UNTRACKED_FILES=$(git ls-files --others --exclude-standard)

if [ -z "$STAGED_FILES" ] && [ -z "$UNSTAGED_FILES" ] && [ -z "$UNTRACKED_FILES" ]; then
    echo "✅ 没有检测到任何变更"
    exit 0
fi

echo ""
echo "📊 变更统计："
echo "  - 已暂存文件: $(echo "$STAGED_FILES" | grep -c . 2>/dev/null || echo 0)"
echo "  - 未暂存文件: $(echo "$UNSTAGED_FILES" | grep -c . 2>/dev/null || echo 0)"
echo "  - 未跟踪文件: $(echo "$UNTRACKED_FILES" | grep -c . 2>/dev/null || echo 0)"
echo ""

# 如果有未暂存的变更，询问是否暂存
if [ -n "$UNSTAGED_FILES" ] || [ -n "$UNTRACKED_FILES" ]; then
    echo "⚠️  发现有未暂存的变更"
    echo ""
    echo "未暂存的文件："
    echo "$UNSTAGED_FILES" | while read -r file; do
        [ -n "$file" ] && echo "  - $file"
    done
    echo ""
    echo "未跟踪的文件："
    echo "$UNTRACKED_FILES" | while read -r file; do
        [ -n "$file" ] && echo "  - $file"
    done
    echo ""
    
    read -p "是否暂存所有变更? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add -A
        echo "✅ 已暂存所有变更"
    else
        echo "ℹ️  将只提交已暂存的变更"
    fi
    echo ""
fi

# 获取差异内容进行分析
DIFF_STATS=$(git diff --cached --stat 2>/dev/null || echo "")
DIFF_CONTENT=$(git diff --cached 2>/dev/null | head -100 || echo "")

if [ -z "$DIFF_STATS" ]; then
    echo "❌ 没有已暂存的变更"
    exit 1
fi

echo "📝 正在生成 Commit Message..."
echo ""

# 自动分析变更类型
analyze_changes() {
    local diff="$1"
    local type=""
    local scope=""
    
    # 检测新增文件
    if echo "$diff" | grep -q "new file mode"; then
        type="feat"
    # 检测删除文件
    elif echo "$diff" | grep -q "deleted file mode"; then
        type="refactor"
    # 检测测试文件
    elif echo "$diff" | grep -qE "test|spec|\.test\.|\.spec\."; then
        type="test"
    # 检测文档文件
    elif echo "$diff" | grep -qE "README|CHANGELOG|\.md$|docs/"; then
        type="docs"
    # 检测配置文件
    elif echo "$diff" | grep -qE "\.json$|\.yml$|\.yaml$|\.config\.|Dockerfile|\.env"; then
        type="chore"
    # 检测修复相关关键词
    elif echo "$diff" | grep -qiE "fix|bug|error|issue|resolve"; then
        type="fix"
    # 默认为新功能
    else
        type="feat"
    fi
    
    echo "$type"
}

# 提取 scope（从文件路径）
extract_scope() {
    local files="$1"
    local first_file=$(echo "$files" | head -1)
    
    # 尝试从路径提取 scope
    if echo "$first_file" | grep -qE "^src/|^lib/|^app/"; then
        echo "$first_file" | sed -E 's#^(src|lib|app)/([^/]+)/.*#\2#' | head -1
    elif echo "$first_file" | grep -qE "^components/|^pages/|^utils/"; then
        echo "$first_file" | cut -d'/' -f2
    else
        echo ""
    fi
}

# 自动生成类型
COMMIT_TYPE=$(analyze_changes "$DIFF_CONTENT")
COMMIT_SCOPE=$(extract_scope "$STAGED_FILES")

echo "🎯 建议的 Commit Message："
echo ""

# 显示建议的 commit message
if [ -n "$COMMIT_SCOPE" ]; then
    SUGGESTED_MSG="$COMMIT_TYPE($COMMIT_SCOPE): "
else
    SUGGESTED_MSG="$COMMIT_TYPE: "
fi

echo "  格式: <type>(<scope>): <subject>"
echo ""
echo "  类型: $COMMIT_TYPE"
echo "  范围: ${COMMIT_SCOPE:-<可选>}"
echo ""
echo "  建议: $SUGGESTED_MSG<描述你的变更>"
echo ""

# 提供交互式输入
read -p "请输入变更描述 (或按 Enter 跳过自动提交): " SUBJECT

if [ -z "$SUBJECT" ]; then
    echo ""
    echo "💡 提示: 你可以手动执行以下命令："
    echo "   git commit -m \"$SUGGESTED_MSG<你的描述>\""
    exit 0
fi

# 构建完整的 commit message
if [ -n "$COMMIT_SCOPE" ]; then
    FULL_MSG="$COMMIT_TYPE($COMMIT_SCOPE): $SUBJECT"
else
    FULL_MSG="$COMMIT_TYPE: $SUBJECT"
fi

echo ""
echo "📝 完整的 Commit Message:"
echo "   $FULL_MSG"
echo ""

# 询问是否提交
read -p "确认提交? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "$FULL_MSG"
    echo ""
    echo "✅ 提交成功！"
    echo ""
    echo "📊 提交信息:"
    git log -1 --stat
else
    echo "ℹ️  已取消提交"
    echo "💡 你可以手动执行: git commit -m \"$FULL_MSG\""
fi