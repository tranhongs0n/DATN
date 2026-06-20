# TODO: Setup Persistent Zalo Webhook for Local Development (Replacing Ngrok)

This document outlines the steps to replace the frustrating Ngrok workflow with a permanent webhook forwarding solution using [Smee.io](https://smee.io). This will ensure you never have to update your Zalo Developer Portal Webhook URL again during local development.

## 1. Generate a Smee URL
1. Go to [https://smee.io/](https://smee.io/).
2. Click **"Start a new channel"**.
3. You will be given a unique URL that looks like this: `https://smee.io/aBcDeFgHiJkLmNoP`
4. Copy this URL. **This is your permanent webhook URL.**

## 2. Update Zalo Developer Portal
1. Log in to the [Zalo for Developers Portal](https://developers.zalo.me/).
2. Go to your Zalo App -> **Webhook**.
3. Paste the `https://smee.io/...` URL you just copied into the **Webhook URL** field.
4. Save the configuration. You will *never* need to change this field again.

## 3. Create the Local Forwarder Script
When you have access to your host device, create a new file in your project called `tools/webhook_forwarder.py` and paste the following Python code into it:

```python
import os
import requests
import sseclient
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("SmeeForwarder")

# --- CONFIGURATION ---
# Replace this with the URL you got from smee.io
SMEE_URL = "https://smee.io/YOUR_SMEE_CHANNEL_ID"

# Your local FastAPI webhook endpoint
LOCAL_WEBHOOK_URL = "http://127.0.0.1:8000/zalo/webhook"
# ---------------------

def start_forwarding():
    logger.info(f"Connecting to Smee.io at {SMEE_URL}...")
    logger.info(f"Forwarding payloads to {LOCAL_WEBHOOK_URL}...")
    
    try:
        response = requests.get(SMEE_URL, stream=True, headers={'Accept': 'text/event-stream'})
        client = sseclient.SSEClient(response)
        
        logger.info("✅ Connected! Waiting for Zalo Webhooks...")
        
        for event in client.events():
            if event.event == "ping":
                continue  # Ignore keep-alive pings
                
            try:
                # Smee wraps the original payload in a JSON object
                smee_data = json.loads(event.data)
                
                # Extract the actual payload sent by Zalo (usually in the 'body' key)
                zalo_payload = smee_data.get("body", {})
                headers = smee_data.get("headers", {})
                
                logger.info(f"📥 Received webhook from Smee: {json.dumps(zalo_payload)[:100]}...")
                
                # Forward it to local FastAPI
                local_response = requests.post(
                    LOCAL_WEBHOOK_URL, 
                    json=zalo_payload,
                    headers={"Content-Type": "application/json"}
                )
                
                logger.info(f"📤 Forwarded to local API. Status: {local_response.status_code}")
                
            except Exception as e:
                logger.error(f"Error processing event data: {e}")
                
    except Exception as e:
        logger.error(f"Failed to connect to Smee.io: {e}")

if __name__ == "__main__":
    # Ensure sseclient-py is installed: pip install sseclient-py requests
    start_forwarding()
```

## 4. Install Dependencies
You will need to install the `sseclient-py` library to listen to Server-Sent Events from Smee.
```bash
pip install sseclient-py requests
```

## 5. Daily Development Workflow
From now on, when you sit down to write code, you only need to run two terminal windows:

**Terminal 1 (Your API):**
```bash
python main.py
```

**Terminal 2 (Your Webhook Forwarder):**
```bash
python tools/webhook_forwarder.py
```

Whenever someone messages the Zalo Bot, Zalo hits `smee.io`, which instantly streams the payload down to `webhook_forwarder.py`, which POSTs it directly into your local `localhost:8000/zalo/webhook` endpoint. No more Ngrok URLs!
