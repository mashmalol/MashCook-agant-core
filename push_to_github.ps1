# PowerShell script to push code to GitHub
# Run this script after installing Git

Write-Host "🚀 Pushing code to GitHub..." -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Initialize git if not already initialized
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Cyan
    git init
}

# Add all files (respects .gitignore)
Write-Host "📝 Adding files..." -ForegroundColor Cyan
git add .
Write-Host "📋 Checking what will be committed..." -ForegroundColor Cyan
git status --short

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Cyan
    $commitMessage = "Add Streamlit web UI with API key input and ERC721 contract generation"
    git commit -m $commitMessage
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Yellow
    Write-Host "   All files are already committed" -ForegroundColor Yellow
}

# Rename branch to main
Write-Host "🌿 Setting branch to main..." -ForegroundColor Cyan
git branch -M main

# Check if remote already exists
$remote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Cyan
    git remote add origin https://github.com/mashmalol/python-core-agant-tamplatev1.git
} else {
    Write-Host "ℹ️  Remote already configured: $remote" -ForegroundColor Yellow
}

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "🔗 Repository: https://github.com/mashmalol/python-core-agant-tamplatev1" -ForegroundColor Cyan
} else {
    Write-Host "❌ Push failed. You may need to:" -ForegroundColor Red
    Write-Host "   1. Configure Git credentials" -ForegroundColor Yellow
    Write-Host "   2. Use a personal access token instead of password" -ForegroundColor Yellow
    Write-Host "   3. Check your internet connection" -ForegroundColor Yellow
}

