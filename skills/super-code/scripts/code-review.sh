#!/bin/bash
# code-review.sh - 执行代码审查
# 用法: ./code-review.sh <file-path>

set -e

# 参数检查
if [ $# -lt 1 ]; then
    echo "用法: $0 <file-path>"
    echo ""
    echo "示例:"
    echo "  $0 src/auth.js"
    echo "  $0 src/"
    exit 1
fi

TARGET="$1"

echo "🔍 正在执行代码审查..."
echo "目标: $TARGET"
echo ""

# 检查目标是否存在
if [ ! -e "$TARGET" ]; then
    echo "❌ 错误：目标不存在: $TARGET"
    exit 1
fi

# 定义审查函数
check_code_style() {
    local file="$1"
    echo "### 📐 代码风格检查"
    echo ""
    
    # 检查行长度
    local long_lines=$(awk 'length > 120 {print NR": "$0}' "$file" 2>/dev/null || echo "")
    if [ -n "$long_lines" ]; then
        echo "⚠️  发现过长行 (>120 字符):"
        echo "$long_lines" | head -5
        echo ""
    fi
    
    # 检查尾随空格
    local trailing=$(grep -n ' $' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$trailing" ]; then
        echo "⚠️  发现尾随空格:"
        echo "$trailing"
        echo ""
    fi
    
    # 检查混合制表符和空格
    local mixed=$(grep -P '(^\t+ +| +\t+)' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$mixed" ]; then
        echo "⚠️  发现混合制表符和空格"
        echo ""
    fi
}

check_naming_conventions() {
    local file="$1"
    echo "### 🏷️  命名规范检查"
    echo ""
    
    # 检查变量名（示例：JavaScript）
    if [[ "$file" =~ \.(js|ts|jsx|tsx)$ ]]; then
        # 检查 var 声明
        local var_usage=$(grep -n '\bvar\b' "$file" 2>/dev/null | head -5 || echo "")
        if [ -n "$var_usage" ]; then
            echo "⚠️  建议使用 let/const 替代 var:"
            echo "$var_usage"
            echo ""
        fi
        
        # 检查单字母变量名（除了常见的 i, j, k）
        local single_letter=$(grep -oP '\b(let|const|var)\s+[a-zA-Z]\b' "$file" 2>/dev/null | grep -v '[ijk]$' || echo "")
        if [ -n "$single_letter" ]; then
            echo "⚠️  发现不清晰的单字母变量名:"
            echo "$single_letter"
            echo ""
        fi
    fi
}

check_complexity() {
    local file="$1"
    echo "### 🧩 复杂度检查"
    echo ""
    
    # 检查函数长度
    if [[ "$file" =~ \.(js|ts|py|java|go)$ ]]; then
        local long_functions=""
        
        case "$file" in
            *.py)
                # Python: 检查函数定义
                long_functions=$(awk '/^def / {start=NR; name=$0} /^def / && NR>start+50 {print name}' "$file" 2>/dev/null || echo "")
                ;;
            *.js|*.ts)
                # JavaScript: 检查函数定义
                long_functions=$(awk '/function/ {start=NR} /^}/ && start && NR>start+50 {print "Long function near line " start; start=0}' "$file" 2>/dev/null || echo "")
                ;;
        esac
        
        if [ -n "$long_functions" ]; then
            echo "⚠️  发现过长函数 (>50 行):"
            echo "$long_functions"
            echo "💡 建议：考虑拆分为更小的函数"
            echo ""
        fi
    fi
    
    # 检查嵌套深度
    local deep_nesting=$(awk '{ 
        depth = 0
        for (i = 1; i <= length($0); i++) {
            c = substr($0, i, 1)
            if (c == "{") depth++
            if (c == "}") depth--
        }
        if (depth > 3) print NR": 嵌套深度 " depth
    }' "$file" 2>/dev/null | head -5 || echo "")
    
    if [ -n "$deep_nesting" ]; then
        echo "⚠️  发现深层嵌套 (>3 层):"
        echo "$deep_nesting"
        echo "💡 建议：使用早返回或提取函数"
        echo ""
    fi
}

check_security() {
    local file="$1"
    echo "### 🔒 安全检查"
    echo ""
    
    # 检查硬编码密码
    local passwords=$(grep -in 'password\s*=\s*["\x27]' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$passwords" ]; then
        echo "🚨 警告：发现硬编码密码:"
        echo "$passwords"
        echo ""
    fi
    
    # 检查硬编码 API 密钥
    local api_keys=$(grep -in 'api[_-]?key\s*=\s*["\x27]' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$api_keys" ]; then
        echo "🚨 警告：发现硬编码 API 密钥:"
        echo "$api_keys"
        echo ""
    fi
    
    # 检查 SQL 注入风险
    local sql_injection=$(grep -in 'execute.*+\|query.*+\|sql.*+' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$sql_injection" ]; then
        echo "⚠️  警告：可能的 SQL 注入风险:"
        echo "$sql_injection"
        echo ""
    fi
    
    # 检查 eval 使用
    local eval_usage=$(grep -in '\beval\s*(' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$eval_usage" ]; then
        echo "⚠️  警告：发现 eval 使用（潜在安全风险）:"
        echo "$eval_usage"
        echo ""
    fi
}

check_best_practices() {
    local file="$1"
    echo "### ✨ 最佳实践检查"
    echo ""
    
    # 检查 TODO/FIXME
    local todos=$(grep -in 'TODO\|FIXME\|XXX\|HACK' "$file" 2>/dev/null | head -10 || echo "")
    if [ -n "$todos" ]; then
        echo "📝 发现待办事项:"
        echo "$todos"
        echo ""
    fi
    
    # 检查 console.log
    if [[ "$file" =~ \.(js|ts|jsx|tsx)$ ]]; then
        local console_logs=$(grep -n 'console\.' "$file" 2>/dev/null | head -5 || echo "")
        if [ -n "$console_logs" ]; then
            echo "⚠️  发现 console 语句（记得移除调试代码）:"
            echo "$console_logs"
            echo ""
        fi
    fi
    
    # 检查注释掉的代码
    local commented_code=$(grep -n '^\s*//.*=\|^\s*#.*=' "$file" 2>/dev/null | head -5 || echo "")
    if [ -n "$commented_code" ]; then
        echo "⚠️  发现注释掉的代码（建议删除）:"
        echo "$commented_code"
        echo ""
    fi
}

# 执行审查
if [ -f "$TARGET" ]; then
    # 单个文件
    echo "## 📄 文件审查: $TARGET"
    echo ""
    
    check_code_style "$TARGET"
    check_naming_conventions "$TARGET"
    check_complexity "$TARGET"
    check_security "$TARGET"
    check_best_practices "$TARGET"
    
elif [ -d "$TARGET" ]; then
    # 目录
    echo "## 📁 目录审查: $TARGET"
    echo ""
    
    # 统计
    local total_files=$(find "$TARGET" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.java" -o -name "*.go" \) | wc -l)
    echo "📊 扫描了 $total_files 个代码文件"
    echo ""
    
    # 对每个文件执行审查
    find "$TARGET" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.java" -o -name "*.go" \) | while read -r file; do
        echo "---"
        echo "### 📄 $file"
        check_code_style "$file"
        check_security "$file"
    done
fi

# 总结
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "## 📊 审查总结"
echo ""
echo "✅ 代码审查已完成"
echo ""
echo "💡 建议："
echo "  1. 优先处理 🚨 安全问题"
echo "  2. 修复 ⚠️  警告项"
echo "  3. 考虑 💡 改进建议"
echo ""
echo "📖 详细指南参考: references/refactor-patterns.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"