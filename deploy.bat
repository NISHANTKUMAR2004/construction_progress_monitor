@echo off
REM Deployment helper script for Windows

echo.
echo 🚀 AI Construction Monitor - Deployment Helper
echo ================================================
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do (
    echo ✓ Python version: %%i
)

REM Check if model exists
if exist "model.pth" (
    echo ✓ Model file found (model.pth)
) else (
    echo ❌ Model file NOT found (model.pth)
    exit /b 1
)

echo.
echo Checking Python dependencies...
pip list | find "streamlit" > nul && echo ✓ streamlit found
pip list | find "torch" > nul && echo ✓ torch found
pip list | find "opencv" > nul && echo ✓ opencv found
pip list | find "numpy" > nul && echo ✓ numpy found

echo.
echo Deployment Status: ✅ READY
echo.
echo Choose deployment option:
echo 1. Local: streamlit run app\app.py
echo 2. Docker: docker build -t aerial-monitor . ^&^& docker run -p 8501:8501 aerial-monitor
echo 3. Docker Compose: docker-compose up
echo 4. Streamlit Cloud: git push ^&^& connect on streamlit.io/cloud
echo.
pause
