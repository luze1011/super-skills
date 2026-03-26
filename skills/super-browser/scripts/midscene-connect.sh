#!/bin/bash
# midscene-connect.sh - Midscene AI 视觉控制脚本
# 用法: ./midscene-connect.sh [command] [options]

set -e

# 默认配置
CDP_PORT=${CDP_PORT:-9222}
BRIDGE_PORT=${BRIDGE_PORT:-3766}
DEFAULT_URL="https://example.com"

# 帮助信息
show_help() {
    cat << EOF
Midscene AI 视觉控制脚本

用法:
    $0 connect [url]              # 新建浏览器连接
    $0 connect-cdp [url]          # CDP 模式连接现有浏览器
    $0 connect-bridge [url]       # Bridge 模式连接
    $0 act "prompt"               # 执行自然语言操作
    $0 screenshot [file]          # 截图
    $0 disconnect                 # 断开连接（不关闭浏览器）
    $0 close                      # 关闭浏览器

环境变量:
    MIDSCENE_MODEL_API_KEY        # AI 模型 API Key
    MIDSCENE_MODEL_NAME           # 模型名称
    MIDSCENE_MODEL_BASE_URL       # API 端点
    MIDSCENE_MODEL_FAMILY         # 模型系列

示例:
    # 新建浏览器并操作
    $0 connect https://github.com
    $0 act "点击登录按钮"
    $0 screenshot login-page.png
    $0 close

    # 连接现有 Chrome（需启用远程调试）
    chrome --remote-debugging-port=9222 &
    $0 connect-cdp https://github.com
    $0 act "点击右上角的 Sign in"
    $0 disconnect

EOF
}

# 检查环境
check_env() {
    if [ -z "$MIDSCENE_MODEL_API_KEY" ]; then
        echo "⚠️  警告: MIDSCENE_MODEL_API_KEY 未设置"
        echo "   请设置环境变量或在脚本中配置"
    fi
}

# 检查 CDP 端口
check_cdp() {
    local code=$(curl -s --max-time 2 -o /dev/null -w "%{http_code}" \
        -H "Upgrade: websocket" \
        http://127.0.0.1:$CDP_PORT/devtools/browser 2>/dev/null || echo "000")
    
    if [ "$code" = "101" ]; then
        echo "✅ CDP 端口 $CDP_PORT 可用"
        return 0
    else
        echo "❌ CDP 端口 $CDP_PORT 不可用 (HTTP $code)"
        echo "   请确保 Chrome 以 --remote-debugging-port=$CDP_PORT 启动"
        return 1
    fi
}

# 检查 Bridge 端口
check_bridge() {
    local code=$(curl -s --max-time 2 -o /dev/null -w "%{http_code}" \
        "http://127.0.0.1:$BRIDGE_PORT/socket.io/?EIO=4&transport=polling" 2>/dev/null || echo "000")
    
    if [ "$code" = "200" ] || [ "$code" = "400" ]; then
        echo "✅ Bridge 端口 $BRIDGE_PORT 可用"
        return 0
    else
        echo "❌ Bridge 端口 $BRIDGE_PORT 不可用"
        echo "   请确保 Midscene 浏览器扩展已安装并启用"
        return 1
    fi
}

# 新建浏览器连接
cmd_connect() {
    local url="${1:-$DEFAULT_URL}"
    echo "🌐 连接到: $url"
    npx @midscene/web@1 connect --url "$url"
}

# CDP 模式连接
cmd_connect_cdp() {
    local url="${1:-$DEFAULT_URL}"
    check_cdp || exit 1
    echo "🌐 CDP 模式连接到: $url"
    npx @midscene/web@1 connect \
        --cdp "ws://127.0.0.1:$CDP_PORT/devtools/browser" \
        --url "$url"
}

# Bridge 模式连接
cmd_connect_bridge() {
    local url="${1:-$DEFAULT_URL}"
    check_bridge || exit 1
    echo "🌐 Bridge 模式连接到: $url"
    npx @midscene/web@1 --bridge connect --url "$url"
}

# 执行操作
cmd_act() {
    local prompt="$1"
    if [ -z "$prompt" ]; then
        echo "❌ 请提供操作提示"
        echo "   用法: $0 act \"点击登录按钮\""
        exit 1
    fi
    echo "🤖 执行: $prompt"
    npx @midscene/web@1 act --prompt "$prompt"
}

# 截图
cmd_screenshot() {
    local file="${1:-screenshot.png}"
    echo "📸 截图保存到: $file"
    npx @midscene/web@1 take_screenshot --output "$file"
}

# 断开连接
cmd_disconnect() {
    echo "🔌 断开连接"
    npx @midscene/web@1 disconnect
}

# 关闭浏览器
cmd_close() {
    echo "🚪 关闭浏览器"
    npx @midscene/web@1 close
}

# 主入口
check_env

case "${1:-help}" in
    connect)
        shift
        cmd_connect "$@"
        ;;
    connect-cdp)
        shift
        cmd_connect_cdp "$@"
        ;;
    connect-bridge)
        shift
        cmd_connect_bridge "$@"
        ;;
    act)
        shift
        cmd_act "$@"
        ;;
    screenshot)
        shift
        cmd_screenshot "$@"
        ;;
    disconnect)
        cmd_disconnect
        ;;
    close)
        cmd_close
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令: $1"
        show_help
        exit 1
        ;;
esac