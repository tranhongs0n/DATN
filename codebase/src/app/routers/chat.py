from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from typing import List, Dict, Any

from src.core.chat_service import chat_response
from src.core import chat_db
from src.app.dependencies import check_rate_limit, logger

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]

@router.post("")
async def chat_endpoint(req: ChatRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"chat_{client_ip}")
    
    logger.info(f"Received chat request: {req.message[:100]}...")
    def event_generator():
        try:
            for response_text in chat_response(req.message, req.history):
                data = json.dumps({"text": response_text}, ensure_ascii=False)
                yield f"data: {data}\n\n"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
            yield f"data: [DONE]\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

class FeedbackRequest(BaseModel):
    message_id: int
    rating: int

@router.post("/feedback")
async def chat_feedback(req: FeedbackRequest):
    chat_db.rate_message(req.message_id, req.rating)
    return {"status": "success"}
