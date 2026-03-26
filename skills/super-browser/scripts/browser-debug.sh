#!/bin/bash
# browser-debug.sh - 浏览器调试分析脚本
# 用法: ./browser-debug.sh [command] [options]

set -e

# 帮助信息
show_help() {
    cat << EOF
浏览器调试分析脚本

用法:
    $0 trace-start              # 开始性能追踪
    $0 trace-stop [file]        # 停止追踪并保存
    $0 network [filter]         # 查看网络请求
    $0 console [level]          # 查看控制台日志
    $0 route-add <pattern>      # 添加网络拦截
    $0 route-clear              # 清除网络拦截
    $0 eval "<js>"              # 执行 JavaScript
    $0 performance              # 性能快照
    $0 memory                   # 内存快照
    $0 coverage                 # 代码覆盖率

调试工作流:
    # 性能分析
    $0 trace-start
    # ... 执行页面操作 ...
    $0 trace-stop trace.json

    # 网络调试
    $0 network
    $0 network "api"            # 筛选 API 请求
    $0 console error            # 只看错误

    # 网络模拟
    $0 route-add "**/*.jpg" --status=404
    $0 route-add "https://api.example.com/**" --mock='{"mock":true}'
    $0 route-clear

EOF
}

# 开始性能追踪
cmd_trace_start() {
    echo "📊 开始性能追踪..."
    playwright-cli tracing-start
}

# 停止追踪
cmd_trace_stop() {
    local file="${1:-trace.zip}"
    echo "📊 停止追踪，保存到: $file"
    playwright-cli tracing-stop
}

# 查看网络
cmd_network() {
    local filter="$1"
    echo "📡 网络请求:"
    if [ -n "$filter" ]; then
        playwright-cli network --filter "$filter"
    else
        playwright-cli network
    fi
}

# 查看控制台
cmd_console() {
    local level="${1:-all}"
    echo "🖥️ 控制台日志 (级别: $level):"
    playwright-cli console --level "$level"
}

# 添加路由拦截
cmd_route_add() {
    local pattern="$1"
    shift
    if [ -z "$pattern" ]; then
        echo "❌ 请提供 URL 模式"
        exit 1
    fi
    echo "🚧 添加路由拦截: $pattern"
    playwright-cli route "$pattern" "$@"
}

# 清除路由
cmd_route_clear() {
    echo "🧹 清除所有路由拦截"
    playwright-cli route-clear
}

# 执行 JavaScript
cmd_eval() {
    local script="$1"
    if [ -z "$script" ]; then
        echo "❌ 请提供 JavaScript 代码"
        exit 1
    fi
    echo "🔧 执行 JavaScript:"
    playwright-cli eval "$script"
}

# 性能快照
cmd_performance() {
    echo "📈 性能快照:"
    playwright-cli eval "
        const timing = performance.timing;
        const metrics = {
            dns: timing.domainLookupEnd - timing.domainLookupStart,
            tcp: timing.connectEnd - timing.connectStart,
            request: timing.responseStart - timing.requestStart,
            response: timing.responseEnd - timing.responseStart,
            dom: timing.domComplete - timing.domLoading,
            total: timing.loadEventEnd - timing.navigationStart
        };
        JSON.stringify(metrics, null, 2);
    "
}

# 内存快照
cmd_memory() {
    echo "💾 内存快照:"
    playwright-cli eval "
        if (performance.memory) {
            JSON.stringify({
                usedJSHeapSize: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024) + ' MB',
                totalJSHeapSize: Math.round(performance.memory.totalJSHeapSize / 1024 / 1024) + ' MB',
                jsHeapSizeLimit: Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024) + ' MB'
            }, null, 2);
        } else {
            'Memory API 不可用';
        }
    "
}

# 代码覆盖率
cmd_coverage() {
    echo "📊 代码覆盖率:"
    playwright-cli coverage
}

# 主入口
case "${1:-help}" in
    trace-start) cmd_trace_start ;;
    trace-stop) shift; cmd_trace_stop "$@" ;;
    network) shift; cmd_network "$@" ;;
    console) shift; cmd_console "$@" ;;
    route-add) shift; cmd_route_add "$@" ;;
    route-clear) cmd_route_clear ;;
    eval) shift; cmd_eval "$@" ;;
    performance) cmd_performance ;;
    memory) cmd_memory ;;
    coverage) cmd_coverage ;;
    help|--help|-h) show_help ;;
    *)
        echo "❌ 未知命令: $1"
        show_help
        exit 1
        ;;
esac