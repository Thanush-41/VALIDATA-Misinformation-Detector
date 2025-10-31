# VALIDATA Deployment Helper Script (PowerShell)
# This script helps prepare your application for deployment

Write-Host "VALIDATA Deployment Helper" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-Not (Test-Path "README.md")) {
    Write-Host "ERROR: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "Pre-deployment Checklist" -ForegroundColor Yellow
Write-Host ""

# 1. Check Git status
Write-Host "1. Checking Git status..."
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "WARNING: You have uncommitted changes. Commit them before deploying." -ForegroundColor Yellow
    git status --short
} else {
    Write-Host "OK: No uncommitted changes" -ForegroundColor Green
}
Write-Host ""

# 2. Check if on main branch
$branch = git rev-parse --abbrev-ref HEAD
Write-Host "2. Current branch: $branch"
if ($branch -ne "main") {
    Write-Host "WARNING: You're not on the main branch. Consider switching to main." -ForegroundColor Yellow
}
Write-Host ""

# 3. Check Python dependencies
Write-Host "3. Checking Python dependencies..."
if (Test-Path "app\FakeNewsDetectorAPI\requirements.txt") {
    Write-Host "OK: requirements.txt found" -ForegroundColor Green
    Write-Host "   Dependencies:"
    Get-Content "app\FakeNewsDetectorAPI\requirements.txt" | Where-Object { $_ -notmatch "^#" -and $_ -ne "" }
} else {
    Write-Host "ERROR: requirements.txt not found" -ForegroundColor Red
}
Write-Host ""

# 4. Check Node dependencies
Write-Host "4. Checking Node dependencies..."
if (Test-Path "app\fake-news-detector-frontend\package.json") {
    Write-Host "OK: package.json found" -ForegroundColor Green
} else {
    Write-Host "ERROR: package.json not found" -ForegroundColor Red
}
Write-Host ""

# 5. Check deployment files
Write-Host "5. Checking deployment configuration files..."
$files = @(
    "app\FakeNewsDetectorAPI\Procfile",
    "app\FakeNewsDetectorAPI\runtime.txt",
    "app\FakeNewsDetectorAPI\render.yaml",
    "app\fake-news-detector-frontend\vercel.json",
    "DEPLOYMENT.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "OK: $file" -ForegroundColor Green
    } else {
        Write-Host "MISSING: $file" -ForegroundColor Red
    }
}
Write-Host ""

# 6. Check environment variables
Write-Host "6. Checking environment setup..."
if (Test-Path "app\fake-news-detector-frontend\.env.example") {
    Write-Host "OK: .env.example found" -ForegroundColor Green
    Write-Host "   Remember to set these variables in Vercel:"
    Get-Content "app\fake-news-detector-frontend\.env.example"
} else {
    Write-Host "WARNING: .env.example not found" -ForegroundColor Yellow
}
Write-Host ""

# 7. Check models directory
Write-Host "7. Checking ML models..."
if (Test-Path "app\FakeNewsDetectorAPI\models") {
    Write-Host "OK: models directory found" -ForegroundColor Green
    Get-ChildItem "app\FakeNewsDetectorAPI\models" | Format-Table Name, Length, LastWriteTime
} else {
    Write-Host "ERROR: models directory not found" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host ""
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. Generate a Django SECRET_KEY:"
Write-Host "   Visit: https://djecrety.ir/"
Write-Host ""
Write-Host "2. Deploy Backend to Render:"
Write-Host "   a. Go to https://render.com"
Write-Host "   b. Create new Web Service"
Write-Host "   c. Connect GitHub repo: Thanush-41/VALIDATA-Misinformation-Detector"
Write-Host "   d. Set root directory: app/FakeNewsDetectorAPI"
Write-Host "   e. Add environment variables (see DEPLOYMENT.md)"
Write-Host ""
Write-Host "3. Deploy Frontend to Vercel:"
Write-Host "   a. Go to https://vercel.com"
Write-Host "   b. Import GitHub repo"
Write-Host "   c. Set root directory: app/fake-news-detector-frontend"
Write-Host "   d. Add REACT_APP_API_URL environment variable"
Write-Host ""
Write-Host "4. Read full deployment guide:"
Write-Host "   Get-Content DEPLOYMENT.md | more"
Write-Host ""
Write-Host "Good luck with your deployment!" -ForegroundColor Green
Write-Host ""
