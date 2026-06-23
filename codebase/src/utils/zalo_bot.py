import hmac
import logging
import requests
from src.config.settings import settings

logger = logging.getLogger(__name__)

MAX_TEXT_LEN = 2000


class ZaloBot:
    def __init__(self):
        self.token = settings.ZALO_BOT_TOKEN
        self.secret_token = settings.ZALO_BOT_SECRET_TOKEN
        self.base_url = "https://bot-api.zaloplatforms.com"

    def verify_secret(self, header_value: str) -> bool:
        if not self.secret_token:
            logger.warning("ZALO_BOT_SECRET_TOKEN not set — webhook secret NOT verified. Set it in production.")
            return True
        if not header_value:
            logger.warning("Zalo Bot webhook missing X-Bot-Api-Secret-Token header.")
            return False
        return hmac.compare_digest(header_value, self.secret_token)

    def _chunks(self, text: str):
        text = text or ""
        for i in range(0, len(text), MAX_TEXT_LEN):
            yield text[i:i + MAX_TEXT_LEN]

    def send_message(self, chat_id: str, text: str) -> bool:
        if not self.token:
            logger.warning("ZALO_BOT_TOKEN is not set. Cannot send message.")
            return False

        url = f"{self.base_url}/bot{self.token}/sendMessage"
        ok = True
        for chunk in self._chunks(text) or [""]:
            if not chunk:
                continue
            try:
                response = requests.post(url, json={"chat_id": chat_id, "text": chunk}, timeout=30)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    logger.error(f"Zalo Bot API error: {data}")
                    ok = False
            except Exception as e:
                logger.error(f"Failed to send Zalo Bot message: {e}")
                ok = False
        return ok

    def get_updates(self, offset: int = None, timeout: int = 30) -> list:
        if not self.token:
            logger.warning("ZALO_BOT_TOKEN is not set. Cannot get updates.")
            return []
            
        url = f"{self.base_url}/bot{self.token}/getUpdates"
        params = {"timeout": timeout}
        if offset is not None:
            params["offset"] = offset
            
        try:
            response = requests.post(url, json=params, timeout=timeout + 5)
            response.raise_for_status()
            data = response.json()
            if data.get("ok"):
                return data.get("result", [])
            else:
                logger.error(f"Zalo Bot getUpdates error: {data}")
        except Exception as e:
            logger.error(f"Failed to fetch updates: {e}")
            
        return []
