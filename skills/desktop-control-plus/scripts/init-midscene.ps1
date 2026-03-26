# Midscene 环境变量初始化脚本
# 使用方法: . .\scripts\init-midscene.ps1

Write-Host "初始化 Midscene 环境变量..." -ForegroundColor Cyan

$env:MIDSCENE_MODEL_API_KEY = "sk-sp-fe2b1e4bcf2247f4b7aa0994832e9f42"
$env:MIDSCENE_MODEL_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
$env:MIDSCENE_MODEL_NAME = "qwen3.5-plus"
$env:MIDSCENE_MODEL_FAMILY = "qwen3.5"
$env:MIDSCENE_MODEL_REASONING_ENABLED = "false"

Write-Host "✅ Midscene 环境变量已设置" -ForegroundColor Green
Write-Host "   MODEL: $env:MIDSCENE_MODEL_NAME" -ForegroundColor Gray
Write-Host "   FAMILY: $env:MIDSCENE_MODEL_FAMILY" -ForegroundColor Gray

# 验证
Write-Host "`n验证配置:" -ForegroundColor Cyan
npx @midscene/computer@1 list_displays 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Midscene 连接成功" -ForegroundColor Green
} else {
    Write-Host "❌ Midscene 连接失败" -ForegroundColor Red
}