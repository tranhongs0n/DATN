from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Depends, Header
from fastapi.responses import StreamingResponse, JSONResponse
import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import shutil
from typing import List, Dict, Any

from src.core.chat_service import chat_service_response as chat_response, db_manager # Alias to avoid confusion if needed
from src.core.chat_service import chat_response, db_manager
from src.core.indexing import IndexingService
from src.utils.document_loader import DocumentLoader
from src.config.settings import settings
from src.utils.zalo_api import ZaloAPI
from src.utils.logger_setup import setup_logger
from src.core import auth
from src.core import chat_db

import time
from collections import defaultdict

app = FastAPI(title="DATN RAG API")
logger = setup_logger("DATN-API")
zalo_api = ZaloAPI()

# Simple in-memory rate limiter
RATE_LIMIT_WINDOW = 60 # seconds
RATE_LIMIT_MAX_REQUESTS = 10
request_counts = defaultdict(list)

def check_rate_limit(client_id: str):
    now = time.time()
    requests = request_counts[client_id]
    # Filter out old requests
    requests = [req_time for req_time in requests if now - req_time < RATE_LIMIT_WINDOW]
    request_counts[client_id] = requests
    if len(requests) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    request_counts[client_id].append(now)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize indexing service
loader = DocumentLoader()
indexing_service = IndexingService(db_manager, loader)

# Auth dependency
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    user = auth.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    user_id = auth.authenticate_user(req.username, req.password)
    if not user_id:
        raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu")
    token = auth.create_session(user_id)
    return {"status": "success", "token": token}

@app.post("/api/auth/logout")
async def logout(current_user: dict = Depends(get_current_user), authorization: str = Header(None)):
    token = authorization.split(" ")[1]
    auth.logout_session(token)
    return {"status": "success"}

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "user": current_user}

@app.get("/api/admin/users")
async def get_users(current_user: dict = Depends(get_current_user)):
    return {"users": auth.get_all_users()}

@app.post("/api/admin/users")
async def create_user(req: LoginRequest, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        logger.warning(f"AUDIT FAILED: User {current_user['username']} attempted to create user without admin role.")
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền tạo tài khoản")
        
    success = auth.create_user(req.username, req.password)
    if not success:
        raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại")
    logger.info(f"AUDIT: User {current_user['username']} created new account for {req.username}")
    return {"status": "success"}

@app.delete("/api/admin/users/{user_id}")
async def delete_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        logger.warning(f"AUDIT FAILED: User {current_user['username']} attempted to delete user {user_id} without admin role.")
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền xóa tài khoản")
        
    if current_user["id"] == user_id:
        raise HTTPException(status_code=400, detail="Không thể xóa chính mình")
    auth.delete_user(user_id)
    logger.info(f"AUDIT: User {current_user['username']} deleted account ID {user_id}")
    return {"status": "success"}

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"chat_{client_ip}")
    
    logger.info(f"Received chat request: {req.message[:100]}...")
    def event_generator():
        try:
            for response_text in chat_response(req.message, req.history):
                # We yield the full text at each step
                data = json.dumps({"text": response_text}, ensure_ascii=False)
                yield f"data: {data}\n\n"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
            yield f"data: [DONE]\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

class ZaloWebhookRequest(BaseModel):
    event_name: str
    app_id: str
    sender: Dict[str, str]
    recipient: Dict[str, str]
    message: Dict[str, Any]
    timestamp: str

@app.post("/zalo/webhook")
async def zalo_webhook(req: Request):
    """
    Webhook endpoint to receive messages from Zalo OA.
    Zalo sends a POST request with JSON payload.
    """
    try:
        data = await req.json()
        event_name = data.get("event_name")
        sender = data.get("sender", {})
        message = data.get("message", {})
        logger.info(f"Zalo webhook received event: {event_name}")
        
        # We only care about user messages
        if event_name == "user_send_text":
            user_id = sender.get("id")
            text = message.get("text", "")
            
            logger.info(f"Zalo user message from {user_id}: {text[:100]}...")
            
            if user_id and text:
                # Handle hidden query button payloads
                if text == "#feedback_up":
                    logger.info(f"User {user_id} gave 👍 feedback via Zalo")
                    zalo_api.send_text_message(user_id, "Cảm ơn bạn đã đánh giá! Phản hồi của bạn giúp tôi học hỏi tốt hơn.")
                    return {"status": "success"}
                elif text == "#feedback_down":
                    logger.info(f"User {user_id} gave 👎 feedback via Zalo")
                    zalo_api.send_text_message(user_id, "Cảm ơn bạn đã góp ý. Tôi sẽ ghi nhận để nhóm phát triển cải thiện.")
                    return {"status": "success"}
                elif text == "#human_handover":
                    chat_db.flag_needs_human(f"zalo_{user_id}")
                    zalo_api.send_text_message(user_id, "Tôi đã chuyển yêu cầu của bạn đến thầy cô tư vấn viên. Vui lòng đợi trong giây lát.")
                    return {"status": "success"}

                # Check if user is blocked
                if chat_db.is_user_blocked(user_id):
                    logger.info(f"Ignored message from blocked Zalo user {user_id}")
                    return {"status": "success", "message": "User is blocked"}

                try:
                    check_rate_limit(f"zalo_{user_id}")
                except HTTPException:
                    logger.warning(f"Rate limit exceeded for Zalo user {user_id}")
                    return {"status": "error", "message": "Rate limit exceeded"}
                
                # Log incoming user message
                chat_db.log_message(user_id, "user", text)
                
                # Fetch history for context
                history_records = chat_db.get_chat_history(user_id)
                # Filter out the message we just logged, take previous 6
                history_records = history_records[:-1][-6:] 
                history = [{"role": r["role"], "content": r["content"]} for r in history_records]
                
                # 1. Process via RAG
                # For Zalo webhook, we need a synchronous or background task response 
                # because we don't stream to Zalo, we send a single response message.
                # Collect the full response:
                final_response = ""
                # Provide history for memory context
                for current_text in chat_response(text, history):
                    final_response = current_text
                
                # Log outgoing AI message
                chat_db.log_message(user_id, "assistant", final_response)
                
                # 2. Send back to Zalo
                logger.info(f"Sending interactive response to Zalo user {user_id}: {final_response[:100]}...")
                
                # Check for human fallback in response
                if "Xin lỗi, tôi không thể tìm thấy" in final_response or "Vui lòng đợi" in final_response:
                    chat_db.flag_needs_human(f"zalo_{user_id}")
                    zalo_api.send_text_message(user_id, final_response)
                else:
                    buttons = [
                        {
                            "title": "👍 Hữu ích",
                            "type": "oa.query.hide",
                            "payload": "#feedback_up"
                        },
                        {
                            "title": "👎 Chưa đúng",
                            "type": "oa.query.hide",
                            "payload": "#feedback_down"
                        },
                        {
                            "title": "Tư vấn viên",
                            "type": "oa.query.hide",
                            "payload": "#human_handover"
                        }
                    ]
                    zalo_api.send_interactive_message(user_id, final_response, buttons)
                
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error in Zalo Webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/api/admin/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    stats = db_manager.get_stats()
    return {
        "doc_count": stats["doc_count"],
        "chunk_count": stats["chunk_count"],
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "llm_model": settings.GEMINI_MODEL_NAME
    }

@app.get("/api/admin/files")
async def get_files(current_user: dict = Depends(get_current_user)):
    file_data, choices = indexing_service.get_file_status_list()
    # file_data is a list of [basename, status, filepath]
    return {"files": [{"name": f[0], "status": f[1], "path": str(f[2])} for f in file_data]}

@app.post("/api/admin/index/rebuild")
async def rebuild_index(current_user: dict = Depends(get_current_user)):
    logger.info(f"AUDIT: User {current_user['username']} triggered full index rebuild")
    docs = indexing_service.load_all_from_disk()
    if not docs:
        logger.warning("No documents found to index during rebuild")
        return {"status": "error", "message": "Không tìm thấy tài liệu nào để index."}
    db_manager.build_from_documents(docs)
    logger.info(f"Successfully rebuilt index with {len(docs)} documents")
    return {"status": "success", "message": f"Hoàn thành xây dựng Index với {len(docs)} tài liệu!"}

@app.post("/api/admin/index/upload")
async def index_upload(files: List[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    if not files:
        return {"status": "error", "message": "Không có tệp nào để xử lý."}
    
    file_names = [f.filename for f in files]
    logger.info(f"Admin uploaded files for indexing: {file_names}")
    
    # Save files locally first
    target_dir = settings.DATA_DIR / "AdminUploads"
    os.makedirs(target_dir, exist_ok=True)
    
    file_paths = []
    for f in files:
        dest = target_dir / f.filename
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        file_paths.append(str(dest))
        
    docs = indexing_service.load_files_by_path(file_paths)
    if not docs:
        logger.error("No documents could be extracted from uploaded files")
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản."}
        
    db_manager.build_from_documents(docs, append=True)
    logger.info(f"Database successfully updated with {len(docs)} chunks from uploaded files")
    return {"status": "success", "message": f"Đã cập nhật Database thành công với {len(docs)} đoạn!"}

class SelectedFilesRequest(BaseModel):
    files: List[str]

@app.post("/api/admin/index/selected")
async def index_selected(req: SelectedFilesRequest, current_user: dict = Depends(get_current_user)):
    if not req.files:
        return {"status": "error", "message": "Vui lòng chọn ít nhất một tệp."}
        
    logger.info(f"Indexing selected files: {req.files}")
    path_map = indexing_service.get_full_path_map()
    file_paths = [path_map.get(name) for name in req.files if path_map.get(name)]
    docs = indexing_service.load_files_by_path(file_paths)
    
    if not docs:
        logger.error("No documents could be extracted from selected files")
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản từ các tệp đã chọn."}
        
    db_manager.build_from_documents(docs, append=True)
    logger.info(f"Successfully indexed selected files with {len(docs)} chunks")
    return {"status": "success", "message": f"Hoàn thành! Đã index {len(req.files)} tệp."}

@app.get("/api/admin/files/unsupported")
async def get_unsupported_files(current_user: dict = Depends(get_current_user)):
    """Returns a list of files that are not indexable (.pdf, .docx)."""
    # include_assets=True will return all files (images + other extensions)
    all_files = loader.get_available_files(include_assets=True)
    
    unsupported = []
    for f_path in all_files:
        basename = os.path.basename(f_path)
        if not f_path.lower().endswith(('.pdf', '.docx')):
            unsupported.append({
                "name": basename,
                "path": str(f_path),
                "extension": os.path.splitext(basename)[1].lower()
            })
    return {"files": unsupported}

class ConvertRequest(BaseModel):
    filename: str

@app.post("/api/admin/files/convert")
async def convert_file(req: ConvertRequest, current_user: dict = Depends(get_current_user)):
    """Converts an unsupported file to .docx via AI."""
    from src.core.chat_service import engine
    try:
        new_filename = indexing_service.convert_unsupported_file(req.filename, engine)
        return {"status": "success", "message": f"Đã chuyển đổi thành công: {new_filename}", "new_file": new_filename}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi chuyển đổi: {str(e)}"}

@app.post("/api/admin/scrape")
async def start_scrape(category: str = Form("all"), limit: int = Form(10), current_user: dict = Depends(get_current_user)):
    """Triggers the web scraper for TLU Admission portal."""
    from src.utils.scraper import TLUAdmissionScraper
    scraper = TLUAdmissionScraper()
    
    try:
        if category == "all":
            for cat in settings.SCRAPER.categories:
                scraper.scrape_category(cat.model_dump(), limit=limit)
        else:
            # Find the specific category config
            cat_config = next((c for c in settings.SCRAPER.categories if c.name == category), None)
            if not cat_config:
                return {"status": "error", "message": f"Không tìm thấy category: {category}"}
            scraper.scrape_category(cat_config.model_dump(), limit=limit)
            
        logger.info(f"AUDIT: User {current_user['username']} completed Scraping for {category} with limit {limit}")
        return {"status": "success", "message": "Hoàn thành quá trình Scraping!"}
    except Exception as e:
        logger.error(f"AUDIT: User {current_user['username']} encountered Scraping Error: {str(e)}")
        return {"status": "error", "message": f"Lỗi Scraping: {str(e)}"}

@app.post("/api/admin/files/convert-all")
async def convert_all_files(current_user: dict = Depends(get_current_user)):
    """Bulk converts all unsupported files to .docx."""
    from src.core.chat_service import engine
    
    unsupported_files = loader.get_available_files(include_assets=True)
    unsupported_files = [f for f in unsupported_files if not f.lower().endswith(('.pdf', '.docx'))]
    
    if not unsupported_files:
        return {"status": "warning", "message": "Không có tệp nào cần chuyển đổi."}
        
    converted = 0
    errors = 0
    
    for f_path in unsupported_files:
        try:
            indexing_service.convert_unsupported_file(os.path.basename(f_path), engine)
            converted += 1
        except Exception as e:
            logger.error(f"Failed to convert {f_path}: {e}")
            errors += 1
            
    return {
        "status": "success", 
        "message": f"Chuyển đổi hoàn tất: {converted} thành công, {errors} lỗi."
    }

# Zalo Chat History endpoints
@app.get("/api/admin/conversations")
async def get_conversations(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "conversations": chat_db.get_conversations()}

@app.get("/api/admin/conversations/{user_id}")
async def get_conversation_history(user_id: str, current_user: dict = Depends(get_current_user)):
    return {"status": "success", "history": chat_db.get_chat_history(user_id)}

class ManualReplyRequest(BaseModel):
    message: str

@app.post("/api/admin/conversations/{user_id}/reply")
async def send_manual_reply(user_id: str, req: ManualReplyRequest, current_user: dict = Depends(get_current_user)):
    success = zalo_api.send_text_message(user_id, req.message)
    if success:
        chat_db.log_message(user_id, "admin", req.message)
        chat_db.clear_human_flag(user_id)
        return {"status": "success"}
    return {"status": "error", "message": "Failed to send message"}

class FeedbackRequest(BaseModel):
    message_id: int
    rating: int  # 1 for thumbs up, -1 for thumbs down

@app.post("/api/chat/feedback")
async def chat_feedback(req: FeedbackRequest):
    chat_db.rate_message(req.message_id, req.rating)
    return {"status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "vector_db": "connected", "api": "running"}

@app.get("/api/admin/export/chats")
async def export_chats(current_user: dict = Depends(get_current_user)):
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "User ID", "Role", "Content", "Timestamp", "Needs Human", "Rating"])
    
    conn = sqlite3.connect(chat_db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, role, content, timestamp, needs_human, rating FROM messages ORDER BY timestamp DESC")
    for row in cursor.fetchall():
        writer.writerow(row)
    conn.close()
    
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=chat_export.csv"
    return response

@app.get("/api/admin/export/documents")
async def export_documents(current_user: dict = Depends(get_current_user)):
    import csv
    from io import StringIO
    
    file_data, _ = indexing_service.get_file_status_list()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Filename", "Status", "Path"])
    
    for f in file_data:
        writer.writerow([f[0], f[1], f[2]])
        
    response = StreamingResponse(iter([output.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=document_export.csv"
    return response

class BlockUserRequest(BaseModel):
    reason: str = ""

@app.post("/api/admin/conversations/{user_id}/block")
async def block_zalo_user(user_id: str, req: BlockUserRequest, current_user: dict = Depends(get_current_user)):
    chat_db.block_user(user_id, req.reason)
    logger.info(f"AUDIT: Admin {current_user['username']} blocked Zalo user {user_id}. Reason: {req.reason}")
    return {"status": "success", "message": f"User {user_id} has been blocked."}

@app.post("/api/admin/conversations/{user_id}/unblock")
async def unblock_zalo_user(user_id: str, current_user: dict = Depends(get_current_user)):
    chat_db.unblock_user(user_id)
    logger.info(f"AUDIT: Admin {current_user['username']} unblocked Zalo user {user_id}.")
    return {"status": "success", "message": f"User {user_id} has been unblocked."}

@app.get("/api/admin/conversations/blocked")
async def get_blocked_list(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "blocked_users": chat_db.get_blocked_users()}

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
