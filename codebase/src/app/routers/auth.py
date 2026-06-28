from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from src.core import auth
from src.app.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("")
@router.post("/login")
async def login(req: LoginRequest):
    user_id = auth.authenticate_user(req.username, req.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")
    token = auth.create_session(user_id)
    return {"status": "success", "token": token}

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user), authorization: str = Header(None)):
    token = authorization.split(" ")[1]
    auth.logout_session(token)
    return {"status": "success"}

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "user": current_user}
