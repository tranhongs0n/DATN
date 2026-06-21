import os
import json
import logging
from pathlib import Path
import requests
import sseclient
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(message)s')

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SMEE_URL = os.environ.get("SMEE_URL", "https://smee.io/M6e71KjdjqYg4g8")
LOCAL_WEBHOOK_URL = os.environ.get("LOCAL_WEBHOOK_URL", "http://127.0.0.1:8000/zalo/bot/webhook")
SECRET_TOKEN = os.environ.get("ZALO_BOT_SECRET_TOKEN", "")


def start_forwarding():
    logging.info(f"Connecting to {SMEE_URL}...")
    headers = {"Content-Type": "application/json"}
    if SECRET_TOKEN:
        headers["X-Bot-Api-Secret-Token"] = SECRET_TOKEN
    try:
        client = sseclient.SSEClient(requests.get(SMEE_URL, stream=True, headers={'Accept': 'text/event-stream'}))
        logging.info(f"Connected. Forwarding to {LOCAL_WEBHOOK_URL}...")
        for event in client.events():
            if event.event != "ping":
                try:
                    payload = json.loads(event.data).get("body", {})
                    logging.info(f"Received: {json.dumps(payload)[:100]}...")
                    r = requests.post(LOCAL_WEBHOOK_URL, json=payload, headers=headers)
                    logging.info(f"Forwarded. Status: {r.status_code}")
                except Exception as e:
                    logging.error(f"Event error: {e}")
    except Exception as e:
        logging.error(f"Connection failed: {e}")


if __name__ == "__main__":
    start_forwarding()
