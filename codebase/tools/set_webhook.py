import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def main():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    token = os.environ.get("ZALO_BOT_TOKEN")
    if not token or token == "thay_token_cua_ban_vao_day" or len(token) < 10:
        print("Error: ZALO_BOT_TOKEN is missing or invalid in .env")
        return

    smee_url = os.environ.get("SMEE_URL", "https://smee.io/M6e71KjdjqYg4g8")
    secret_token = os.environ.get("ZALO_BOT_SECRET_TOKEN", "DATN_ZALO_SECRET_123")
    print(f"Setting Webhook URL: {smee_url} for Zalo Bot...")
    print(f"Using Secret Token: {secret_token}")
    
    url = f"https://bot-api.zaloplatforms.com/bot{token}/setWebhook"
    try:
        r = requests.post(url, json={"url": smee_url, "secret_token": secret_token}, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("ok"):
            print("Success! Zalo Bot webhook is now set to Smee.")
        else:
            print(f"Failed: {data}")
    except Exception as e:
        print(f"API Connection Error: {e}")

if __name__ == "__main__":
    main()
