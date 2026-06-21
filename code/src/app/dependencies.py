from fastapi import Header, HTTPException, Depends
from collections import defaultdict
import time
from src.core import auth
from src.utils.logger_setup import setup_logger
from src.core.chat_service import db_manager
from src.utils.document_loader import DocumentLoader
from src.core.indexing import IndexingService
from src.utils.zalo_api import ZaloAPI

logger = setup_logger("DATN-API")
zalo_api = ZaloAPI()

loader = DocumentLoader()
indexing_service = IndexingService(db_manager, loader)

RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX_REQUESTS = 10
request_counts = defaultdict(list)

def check_rate_limit(client_id: str):
    now = time.time()
    requests = [req_time for req_time in request_counts[client_id] if now - req_time < RATE_LIMIT_WINDOW]
    if len(requests) >= RATE_LIMIT_MAX_REQUESTS:
        request_counts[client_id] = requests
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    requests.append(now)
    request_counts[client_id] = requests
    # Evict empty buckets so the dict doesn't grow unbounded across distinct client_ids.
    if len(request_counts) > 10000:
        for k in [k for k, v in request_counts.items() if not v]:
            del request_counts[k]

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
