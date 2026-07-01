@echo off
echo Starting DATN FastAPI Server and Webhook Forwarder...
cd /d "%~dp0"
start "FastAPI UI" python main.py ui
start "Smee Forwarder" python tools\webhook_forwarder.py
echo Services started in new windows.
pause
