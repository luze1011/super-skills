#!/bin/bash
# Midscene 桌面自动化脚本
# 提供简化的 Midscene 命令封装

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查环境变量
check_env() {
    if [ -z "$MIDSCENE_MODEL_API_KEY" ]; then
        log_error "MIDSCENE_MODEL_API_KEY 未设置"
        echo "请运行: source scripts/init-env.sh"
        exit 1
    fi
    log_success "环境变量已配置"
}

# 连接桌面
connect() {
    check_env
    log_info "连接桌面..."
    npx @midscene/computer@1 connect
}

# 断开连接
disconnect() {
    log_info "断开连接..."
    npx @midscene/computer@1 disconnect
}

# 截图
screenshot() {
    log_info "截图中..."
    npx @midscene/computer@1 take_screenshot
    log_success "截图完成"
}

# 执行动作
act() {
    local prompt="$1"
    local deepThink="${2:-false}"
    
    if [ -z "$prompt" ]; then
        log_error "请提供动作提示词"
        echo "用法: $0 act \"你的指令\" [--deepThink]"
        exit 1
    fi
    
    check_env
    
    if [ "$deepThink" = "true" ] || [ "$deepThink" = "--deepThink" ]; then
        log_info "执行动作（深度思考模式）: $prompt"
        npx @midscene/computer@1 act --prompt "$prompt" --deepThink
    else
        log_info "执行动作: $prompt"
        npx @midscene/computer@1 act --prompt "$prompt"
    fi
    
    log_success "动作执行完成"
}

# 列出显示器
list_displays() {
    log_info "列出显示器..."
    npx @midscene/computer@1 list_displays
}

# 完整工作流
workflow() {
    local prompt="$1"
    
    if [ -z "$prompt" ]; then
        log_error "请提供工作流提示词"
        echo "用法: $0 workflow \"你的指令\""
        exit 1
    fi
    
    log_info "开始工作流: $prompt"
    
    # 1. 连接
    connect
    
    # 2. 执行动作
    act "$prompt"
    
    # 3. 截图确认
    screenshot
    
    # 4. 断开连接
    disconnect
    
    log_success "工作流完成"
}

# 帮助信息
help() {
    echo "Midscene 桌面自动化脚本"
    echo ""
    echo "用法: $0 <command> [args]"
    echo ""
    echo "命令:"
    echo "  connect              连接桌面"
    echo "  disconnect           断开连接"
    echo "  screenshot           截图"
    echo "  act <prompt>         执行动作"
    echo "  act <prompt> --deepThink  执行动作（深度思考）"
    echo "  list_displays        列出显示器"
    echo "  workflow <prompt>    完整工作流（连接→执行→截图→断开）"
    echo "  help                 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 connect"
    echo "  $0 act \"打开记事本，输入 Hello World\""
    echo "  $0 workflow \"在 Chrome 中搜索 Python 教程\""
}

# 主入口
main() {
    case "${1:-help}" in
        connect)
            connect
            ;;
        disconnect)
            disconnect
            ;;
        screenshot)
            screenshot
            ;;
        act)
            act "$2" "$3"
            ;;
        list_displays)
            list_displays
            ;;
        workflow)
            workflow "$2"
            ;;
        help|--help|-h)
            help
            ;;
        *)
            log_error "未知命令: $1"
            help
            exit 1
            ;;
    esac
}

main "$@"