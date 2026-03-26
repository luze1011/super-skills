# 安装所有超级技能
# 使用方法: ./scripts/install-all.ps1

Write-Host "🚀 安装所有超级技能..." -ForegroundColor Cyan

$skills = @(
  "super-browser",
  "super-testing",
  "super-code",
  "super-document",
  "super-search",
  "super-writing-assistant",
  "desktop-control-plus",
  "testing-expert",
  "code-review-suite",
  "creative-generator",
  "marketing-suite"
)

foreach ($skill in $skills) {
  Write-Host "安装 $skill..." -ForegroundColor Yellow
  npx skills add luze1011/super-skills@$skill --yes --global 2>$null
}

Write-Host "`n✅ 安装完成！" -ForegroundColor Green
Write-Host "共安装 $($skills.Count) 个超级技能" -ForegroundColor Cyan