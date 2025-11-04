@echo off
setlocal

echo ==========================================
echo   Python Virtual Environment Setup (Win)
echo ==========================================

rem Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3 first.
    exit /b 1
)

echo [1/4] Creating virtual environment (.venv)...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create venv
    exit /b 1
)

echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/4] Upgrading pip...
pip install --upgrade pip

echo [4/4] Installing dependencies from requirements.ttx...
pip install -r requirements.ttx
if %errorlevel% neq 0 (
    echo ERROR: Dependency installation failed
    exit /b 1
)

echo ✅ Installation complete!
echo To activate environment manually later:
echo     .venv\Scripts\activate
echo ==========================================

endlocal
pause
