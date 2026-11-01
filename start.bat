@echo off
echo Checking for Python...
python --version 2>NUL
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from python.org and ensure you check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo.
echo Installing requirements...
python -m pip install -r requirements.txt

echo.
echo Downloading spaCy model (optional)...
python -m spacy download en_core_web_sm

echo.
echo Starting Application...
start http://127.0.0.1:5000
python app.py
pause
