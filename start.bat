@echo off
echo Starting TLU Admission RAG Services...

:: Ensure we are in the script's directory
cd /d "%~dp0"

:: Start the Webhook Forwarder in a new terminal window
if exist "codebase\tools\webhook_forwarder.py" (
    echo Starting Smee Webhook Forwarder...
    start "Zalo Bot Webhook Forwarder" python codebase\tools\webhook_forwarder.py
) else (
    echo Warning: codebase\tools\webhook_forwarder.py not found. Skipping webhook forwarder.
)

:: Start the Main API Server in the current window
echo Starting FastAPI Server...
echo ========================================================
echo UI is available at: http://localhost:8000
echo Admin is available at: http://localhost:8000/admin
echo ========================================================
cd codebase
python main.py

echo.
echo FastAPI Server has stopped. 
echo Note: You may need to manually close the Webhook Forwarder window.
pause
