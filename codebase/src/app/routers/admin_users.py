from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.core import auth
from src.app.dependencies import require_admin, logger

router = APIRouter(prefix="/api/admin/users", tags=["admin_users"])

class LoginRequest(BaseModel):
    username: str
    password: str

class UpdateUserRequest(BaseModel):
    username: str
    password: str | None = None

@router.get("")
async def get_users(current_user: dict = Depends(require_admin)):
    return {"users": auth.get_all_users()}

@router.post("")
async def create_user(req: LoginRequest, current_user: dict = Depends(require_admin)):
    success = auth.create_user(req.username, req.password)
    if not success:
        raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại")
    logger.info(f"AUDIT: User {current_user['username']} created new account for {req.username}")
    return {"status": "success"}

@router.put("/{user_id}")
async def update_user(user_id: int, req: UpdateUserRequest, current_user: dict = Depends(require_admin)):
    success = auth.update_user(user_id, req.username, req.password)
    if not success:
        raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại hoặc lỗi hệ thống")
    logger.info(f"AUDIT: User {current_user['username']} updated account for {req.username}")
    return {"status": "success"}

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: dict = Depends(require_admin)):
    if current_user["id"] == user_id:
        raise HTTPException(status_code=400, detail="Không thể xóa chính mình")
    auth.delete_user(user_id)
    logger.info(f"AUDIT: User {current_user['username']} deleted account ID {user_id}")
    return {"status": "success"}
