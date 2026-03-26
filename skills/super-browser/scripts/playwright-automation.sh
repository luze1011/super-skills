#!/bin/bash
# playwright-automation.sh - Playwright 精确自动化脚本
# 用法: ./playwright-automation.sh [command] [options]

set -e

# 帮助信息
show_help() {
    cat << EOF
Playwright 精确自动化脚本

用法:
    $0 open <url>                 # 打开浏览器
    $0 snapshot                   # 获取页面快照（元素引用 e1, e2...）
    $0 click <ref>                # 点击元素
    $0 fill <ref> "text"          # 填写文本
    $0 select <ref> "option"      # 选择选项
    $0 check <ref>                # 勾选复选框
    $0 hover <ref>                # 悬停
    $0 press <key>                # 按键
    $0 goto <url>                 # 导航
    $0 reload                     # 刷新
    $0 wait [type]                # 等待（load|networkidle|selector）
    $0 screenshot [file]          # 截图
    $0 state-save <file>          # 保存状态
    $0 state-load <file>          # 加载状态
    $0 network                    # 查看网络请求
    $0 console                    # 查看控制台
    $0 close                      # 关闭浏览器

工作流示例:
    # 基本表单填写
    $0 open https://example.com/form
    $0 snapshot
    $0 fill e1 "john@example.com"
    $0 fill e2 "password123"
    $0 click e3
    $0 close

    # 保存登录状态
    $0 open https://github.com/login
    $0 snapshot
    $0 fill e1 "username"
    $0 fill e2 "password"
    $0 click e3
    $0 state-save github-auth.json
    $0 close

    # 下次自动登录
    $0 open https://github.com
    $0 state-load github-auth.json
    $0 snapshot

EOF
}

# 打开浏览器
cmd_open() {
    local url="$1"
    if [ -z "$url" ]; then
        echo "❌ 请提供 URL"
        exit 1
    fi
    echo "🌐 打开: $url"
    playwright-cli open "$url"
}

# 获取快照
cmd_snapshot() {
    echo "📸 获取页面快照..."
    playwright-cli snapshot
}

# 点击元素
cmd_click() {
    local ref="$1"
    if [ -z "$ref" ]; then
        echo "❌ 请提供元素引用 (如 e1, e2)"
        exit 1
    fi
    echo "👆 点击: $ref"
    playwright-cli click "$ref"
}

# 填写文本
cmd_fill() {
    local ref="$1"
    local text="$2"
    if [ -z "$ref" ] || [ -z "$text" ]; then
        echo "❌ 用法: $0 fill <ref> \"text\""
        exit 1
    fi
    echo "✏️  填写 $ref: $text"
    playwright-cli fill "$ref" "$text"
}

# 选择选项
cmd_select() {
    local ref="$1"
    local option="$2"
    if [ -z "$ref" ] || [ -z "$option" ]; then
        echo "❌ 用法: $0 select <ref> \"option\""
        exit 1
    fi
    echo "📋 选择 $ref: $option"
    playwright-cli select "$ref" "$option"
}

# 勾选复选框
cmd_check() {
    local ref="$1"
    if [ -z "$ref" ]; then
        echo "❌ 请提供元素引用"
        exit 1
    fi
    echo "☑️  勾选: $ref"
    playwright-cli check "$ref"
}

# 悬停
cmd_hover() {
    local ref="$1"
    if [ -z "$ref" ]; then
        echo "❌ 请提供元素引用"
        exit 1
    fi
    echo "🎯 悬停: $ref"
    playwright-cli hover "$ref"
}

# 按键
cmd_press() {
    local key="$1"
    if [ -z "$key" ]; then
        echo "❌ 请提供按键名称 (如 Enter, Escape, Tab)"
        exit 1
    fi
    echo "⌨️  按键: $key"
    playwright-cli press "$key"
}

# 导航
cmd_goto() {
    local url="$1"
    if [ -z "$url" ]; then
        echo "❌ 请提供 URL"
        exit 1
    fi
    echo "🧭 导航到: $url"
    playwright-cli goto "$url"
}

# 刷新
cmd_reload() {
    echo "🔄 刷新页面"
    playwright-cli reload
}

# 等待
cmd_wait() {
    local type="${1:-load}"
    echo "⏳ 等待: $type"
    playwright-cli wait --load "$type"
}

# 截图
cmd_screenshot() {
    local file="${1:-screenshot.png}"
    echo "📸 截图保存到: $file"
    playwright-cli screenshot "$file"
}

# 保存状态
cmd_state_save() {
    local file="$1"
    if [ -z "$file" ]; then
        echo "❌ 请提供文件名"
        exit 1
    fi
    echo "💾 保存状态到: $file"
    playwright-cli state-save "$file"
}

# 加载状态
cmd_state_load() {
    local file="$1"
    if [ -z "$file" ]; then
        echo "❌ 请提供文件名"
        exit 1
    fi
    echo "📂 加载状态: $file"
    playwright-cli state-load "$file"
}

# 查看网络
cmd_network() {
    echo "📡 网络请求:"
    playwright-cli network
}

# 查看控制台
cmd_console() {
    echo "🖥️ 控制台日志:"
    playwright-cli console
}

# 关闭浏览器
cmd_close() {
    echo "🚪 关闭浏览器"
    playwright-cli close
}

# 执行 JavaScript
cmd_eval() {
    local script="$1"
    if [ -z "$script" ]; then
        echo "❌ 请提供 JavaScript 代码"
        exit 1
    fi
    echo "🔧 执行: $script"
    playwright-cli eval "$script"
}

# 主入口
case "${1:-help}" in
    open) shift; cmd_open "$@" ;;
    snapshot) cmd_snapshot ;;
    click) shift; cmd_click "$@" ;;
    fill) shift; cmd_fill "$@" ;;
    select) shift; cmd_select "$@" ;;
    check) shift; cmd_check "$@" ;;
    hover) shift; cmd_hover "$@" ;;
    press) shift; cmd_press "$@" ;;
    goto) shift; cmd_goto "$@" ;;
    reload) cmd_reload ;;
    wait) shift; cmd_wait "$@" ;;
    screenshot) shift; cmd_screenshot "$@" ;;
    state-save) shift; cmd_state_save "$@" ;;
    state-load) shift; cmd_state_load "$@" ;;
    network) cmd_network ;;
    console) cmd_console ;;
    close) cmd_close ;;
    eval) shift; cmd_eval "$@" ;;
    help|--help|-h) show_help ;;
    *)
        echo "❌ 未知命令: $1"
        show_help
        exit 1
        ;;
esac