@echo off
REM Startup script for Smart AI Resume Analyzer (Windows version)

echo Starting Smart AI Resume Analyzer...

REM Check if Chrome is installed silently
where chrome >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Chrome not found. Please install Google Chrome and try again.
    echo You can download Chrome from: https://www.google.com/chrome/
    pause
    exit /b 1
)

REM Run the chromedriver setup script silently
python setup_chromedriver.py >nul 2>nul

REM Start the application
echo Starting application...
streamlit run app.py

pause 