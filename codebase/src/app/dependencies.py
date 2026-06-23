from fastapi import Header, HTTPException, Depends
from collections import defaultdict
import time
from src.core import auth
from src.utils.logger_setup import setup_logger
from src.core.chat_service import db_manager
from src.utils.document_loader import DocumentLoader
from src.core.indexing import IndexingService
from src.utils.zalo_bot import ZaloBot

logger = setup_logger("DATN-API")
zalo_bot = ZaloBot()

loader = DocumentLoader()
indexing_service = IndexingService(db_manager, loader)

import time

class TokenBucket:
    def __init__(self, rate, capacity):
        self.tokens = capacity
        self.capacity = capacity
        self.rate = rate
        self.last_update = time.time()
        
    def consume(self, tokens_needed):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_update) * self.rate)
        self.last_update = now
        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        return False

# Cấu hình Token-Bucket: phục hồi 1 token mỗi 6 giây, sức chứa tối đa 10 token
rate_limiters = defaultdict(lambda: TokenBucket(rate=1/6.0, capacity=10))

def check_rate_limit(client_id: str):
    bucket = rate_limiters[client_id]
    if not bucket.consume(1):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    user = auth.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        logger.warning(f"AUDIT FAILED: User {current_user.get('username')} attempted admin action without admin role.")
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền thực hiện thao tác này")
    return current_user
