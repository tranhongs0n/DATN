import os
import requests
import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)

class ZaloAPI:
    def __init__(self):
        self.access_token = settings.ZALO_ACCESS_TOKEN
        self.base_url = "https://openapi.zalo.me/v2.0/oa/message"

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
