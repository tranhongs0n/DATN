@echo off
echo Starting TLU Admission RAG Services...

:: Ensure we are in the script's directory
cd /d "%~dp0"

:: Start the Webhook Forwarder in a new terminal window
if exist "tools\webhook_forwarder.py" (
    echo Starting Smee Webhook Forwarder...
    start "Zalo Webhook Forwarder" python tools\webhook_forwarder.py
) else (
    echo Warning: tools\webhook_forwarder.py not found. Skipping webhook forwarder.
)

:: Start the Main API Server in the current window
echo Starting FastAPI Server...
python main.py

echo.
echo FastAPI Server has stopped. 
echo Note: You may need to manually close the Webhook Forwarder window.
pause
