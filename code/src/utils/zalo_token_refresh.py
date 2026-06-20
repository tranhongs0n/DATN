import os
import requests
import logging
from src.config.settings import settings

logger = logging.getLogger(__name__)

class ZaloTokenRefresher:
    """
    Utility class to handle Zalo OA OAuth token refreshing.
    Zalo access tokens expire and must be refreshed using a refresh token.
    """
    def __init__(self):
        self.app_id = os.environ.get("ZALO_APP_ID")
        self.secret_key = os.environ.get("ZALO_SECRET_KEY")
        self.refresh_token = os.environ.get("ZALO_REFRESH_TOKEN")
        self.url = "https://oauth.zaloapp.com/v4/oa/access_token"

    def refresh(self):
        if not all([self.app_id, self.secret_key, self.refresh_token]):
            logger.error("Missing Zalo App ID, Secret Key, or Refresh Token in environment.")
            return False

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "secret_key": self.secret_key
        }
        
        data = {
            "app_id": self.app_id,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        try:
            response = requests.post(self.url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()
            
            if "access_token" in result:
                new_access_token = result["access_token"]
                new_refresh_token = result["refresh_token"]
                
                # In a real app, save these to a secure database or update the .env file
                logger.info("Successfully refreshed Zalo token.")
                logger.info(f"New Access Token: {new_access_token[:10]}...")
                logger.info(f"New Refresh Token: {new_refresh_token[:10]}...")
                
                # Update in-memory settings for immediate use
                settings.ZALO_ACCESS_TOKEN = new_access_token
                
                return True
            else:
                logger.error(f"Failed to refresh Zalo token: {result}")
                return False
        except Exception as e:
            logger.error(f"Error during Zalo token refresh request: {e}")
            return False

if __name__ == "__main__":
    refresher = ZaloTokenRefresher()
    refresher.refresh()
