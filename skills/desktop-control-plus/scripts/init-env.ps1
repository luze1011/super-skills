# Desktop Control Plus 环境初始化脚本
# 使用方法: . .\skills\desktop-control-plus\scripts\init-env.ps1

param(
    [switch]$Verify,
    [switch]$Quiet
)

function Write-Log {
    param([string]$Message, [string]$Level = "Info")
    if ($Quiet) { return }
    
    $color = switch ($Level) {
        "Info" { "Cyan" }
        "Success" { "Green" }
        "Warning" { "Yellow" }
        "Error" { "Red" }
        default { "White" }
    }
    Write-Host $Message -ForegroundColor $color
}

# ==================== Midscene 配置 ====================

Write-Log "初始化 Midscene 环境变量..." "Info"

$env:MIDSCENE_MODEL_API_KEY = "sk-sp-fe2b1e4bcf2247f4b7aa0994832e9f42"
$env:MIDSCENE_MODEL_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
$env:MIDSCENE_MODEL_NAME = "qwen3.5-plus"
$env:MIDSCENE_MODEL_FAMILY = "qwen3.5"
$env:MIDSCENE_MODEL_REASONING_ENABLED = "false"

Write-Log "✅ Midscene 环境变量已设置" "Success"
if (-not $Quiet) {
    Write-Host "   MODEL: $env:MIDSCENE_MODEL_NAME" -ForegroundColor Gray
    Write-Host "   FAMILY: $env:MIDSCENE_MODEL_FAMILY" -ForegroundColor Gray
    Write-Host "   BASE_URL: $env:MIDSCENE_MODEL_BASE_URL" -ForegroundColor Gray
}

# ==================== PyAutoGUI 配置 ====================

Write-Log "检查 PyAutoGUI 环境..." "Info"

try {
    $pythonVersion = python --version 2>&1
    Write-Log "Python: $pythonVersion" "Success"
    
    # 检查 pyautogui
    $pyautoguiCheck = python -c "import pyautogui; print(pyautogui.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "PyAutoGUI: v$pyautoguiCheck" "Success"
    } else {
        Write-Log "PyAutoGUI 未安装，正在安装..." "Warning"
        pip install pyautogui pillow
    }
} catch {
    Write-Log "Python 环境检查失败: $_" "Error"
}

# ==================== 验证 ====================

if ($Verify) {
    Write-Log "`n验证配置:" "Info"
    
    # 验证 Midscene
    Write-Log "测试 Midscene 连接..." "Info"
    $midsceneTest = npx @midscene/computer@1 list_displays 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✅ Midscene 连接成功" "Success"
    } else {
        Write-Log "❌ Midscene 连接失败" "Error"
        Write-Host $midsceneTest
    }
    
    # 验证 PyAutoGUI
    Write-Log "测试 PyAutoGUI..." "Info"
    $pyautoguiTest = python -c "import pyautogui; print(f'Screen: {pyautogui.size()}')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✅ PyAutoGUI 正常: $pyautoguiTest" "Success"
    } else {
        Write-Log "❌ PyAutoGUI 测试失败" "Error"
    }
}

# ==================== 快捷函数 ====================

function global:Desktop-Connect {
    npx @midscene/computer@1 connect
}

function global:Desktop-Disconnect {
    npx @midscene/computer@1 disconnect
}

function global:Desktop-Act {
    param([Parameter(Mandatory=$true)][string]$Prompt, [switch]$DeepThink)
    
    if ($DeepThink) {
        npx @midscene/computer@1 act --prompt $Prompt --deepThink
    } else {
        npx @midscene/computer@1 act --prompt $Prompt
    }
}

function global:Desktop-Screenshot {
    npx @midscene/computer@1 take_screenshot
}

function global:Desktop-Mouse {
    param([string]$Action, [int]$X, [int]$Y)
    uvx desktop-agent mouse $Action $X $Y
}

function global:Desktop-Keyboard {
    param([string]$Action, [string]$Text)
    uvx desktop-agent keyboard $Action $Text
}

function global:Desktop-App {
    param([string]$Action, [string]$Name)
    uvx desktop-agent app $Action $Name
}

Write-Log "`n✅ Desktop Control Plus 环境初始化完成" "Success"
Write-Log "快捷函数已加载: Desktop-Connect, Desktop-Act, Desktop-Screenshot, Desktop-Mouse, Desktop-Keyboard, Desktop-App" "Info"