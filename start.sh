#!/bin/bash

echo "Starting TLU Admission RAG Services..."

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Start the Webhook Forwarder in the background
if [ -f "tools/webhook_forwarder.py" ]; then
    echo "Starting Smee Webhook Forwarder..."
    python tools/webhook_forwarder.py &
    FORWARDER_PID=$!
else
    echo "Warning: tools/webhook_forwarder.py not found. Skipping webhook forwarder."
fi

# Start the Main API Server
echo "Starting FastAPI Server..."
python main.py

# When the main server exits (e.g. user presses Ctrl+C), kill the forwarder too
echo "Shutting down services..."
if [ -n "$FORWARDER_PID" ]; then
    kill $FORWARDER_PID
fi
