import os
import hashlib
import hmac
import requests
import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)

class ZaloAPI:
    def __init__(self):
        self.access_token = settings.ZALO_ACCESS_TOKEN
        self.app_secret = settings.ZALO_APP_SECRET
        self.base_url = "https://openapi.zalo.me/v2.0/oa/message"

    def verify_signature(self, app_id: str, raw_body: str, timestamp: str, signature: str) -> bool:
        """Verify Zalo webhook signature.

        Zalo signs each webhook with: mac = sha256(appId + data + timestamp + OASecretKey),
        sent in the `X-ZEvent-Signature` header as "mac=<hex>".
        Returns True if no app_secret is configured (verification disabled in dev),
        but logs a warning so this is never silently relied upon in prod.
        """
        if not self.app_secret:
            logger.warning("ZALO_APP_SECRET not set — webhook signature NOT verified. Set it in production.")
            return True
        if not signature:
            logger.warning("Zalo webhook missing X-ZEvent-Signature header.")
            return False
        received = signature[len("mac="):] if signature.startswith("mac=") else signature
        expected = hashlib.sha256(
            f"{app_id}{raw_body}{timestamp}{self.app_secret}".encode("utf-8")
        ).hexdigest()
        if not hmac.compare_digest(received, expected):
            logger.warning("Zalo webhook signature mismatch — rejecting request.")
            return False
        return True

    def send_text_message(self, user_id: str, message: str) -> bool:
        if not self.access_token:
            logger.warning("ZALO_ACCESS_TOKEN is not set. Cannot send message.")
            return False

        headers = {
            "access_token": self.access_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": message
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("error") == 0:
                logger.info(f"Successfully sent Zalo message to {user_id}")
                return True
            else:
                logger.error(f"Zalo API error: {data.get('message')} (Code: {data.get('error')})")
                return False
        except Exception as e:
            logger.error(f"Failed to send Zalo message: {e}")
            return False

    def send_interactive_message(self, user_id: str, text: str, buttons: list) -> bool:
        if not self.access_token:
            logger.warning("ZALO_ACCESS_TOKEN is not set. Cannot send message.")
            return False

        headers = {
            "access_token": self.access_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "promotion",
                        "elements": [
                            { "type": "text", "content": text }
                        ],
                        "buttons": buttons
                    }
                }
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("error") == 0:
                logger.info(f"Successfully sent Zalo interactive message to {user_id}")
                return True
            else:
                logger.error(f"Zalo API error (interactive): {data.get('message')} (Code: {data.get('error')})")
                return False
        except Exception as e:
            logger.error(f"Failed to send Zalo interactive message: {e}")
            return False
