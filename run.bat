@echo off
echo ============================================================
echo   Mutual Fund Analysis Dashboard - Setup
echo ============================================================
echo.

echo [1/3] Generating Mutual Fund Dataset...
set PYTHONIOENCODING=utf-8
python analysis\generate_data.py
if errorlevel 1 (
    echo ERROR: Data generation failed!
    pause
    exit /b 1
)
echo.

echo [2/3] Running Analysis (Clean, Normalize, Score, Rank)...
python analysis\analyze.py
if errorlevel 1 (
    echo ERROR: Analysis failed!
    pause
    exit /b 1
)
echo.

echo [3/3] Launching Dashboard...
echo.
python run_dashboard.py
pause
