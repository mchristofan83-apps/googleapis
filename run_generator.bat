@echo off
echo Starting Google APIs Generator API...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "generator_api.py" (
    echo Error: generator_api.py not found
    pause
    exit /b 1
)

if not exist "bin\protoc.exe" (
    echo Error: protoc.exe not found in bin directory
    echo Please run the setup first
    pause
    exit /b 1
)

echo Starting API server...
echo API will be available at: http://localhost:5000
echo.
echo Available endpoints:
echo   - API Documentation: http://localhost:5000/
echo   - API Keys: http://localhost:5000/api-keys
echo   - Available APIs: http://localhost:5000/apis
echo.
echo Press Ctrl+C to stop the server
echo.

python generator_api.py

pause
