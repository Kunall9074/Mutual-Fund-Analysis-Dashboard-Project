@echo off
echo ============================================================
echo   Pushing Mutual Fund Analysis Dashboard to GitHub
echo ============================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads first.
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
git init
echo.

echo [2/5] Adding files...
git add .
echo.

echo [3/5] Committing files...
git commit -m "Initial commit: Mutual Fund Analysis Dashboard with Python and Web Interface"
echo.

echo [4/5] Renaming branch to main...
git branch -M main
echo.

echo [5/5] Adding remote origin...
git remote add origin https://github.com/Kunall9074/Mutual-Fund-Analysis-Dashboard-Project.git
echo.

echo [6/5] Pushing to GitHub...
echo (You may be asked to sign in to GitHub in a browser window)
git push -u origin main
echo.

echo ============================================================
echo   Done! check your repo at:
echo   https://github.com/Kunall9074/Mutual-Fund-Analysis-Dashboard-Project
echo ============================================================
pause
