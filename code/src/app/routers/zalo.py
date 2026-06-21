from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import json

from src.core.chat_service import chat_response, response_needs_human
from src.core import chat_db
from src.app.dependencies import get_current_user, zalo_api, logger, check_rate_limit

router = APIRouter(tags=["zalo"])


def _process_user_text(user_id: str, text: str):
    """Handle one inbound Zalo text message. Runs in a threadpool (blocking I/O + LLM)."""
    # Quick-reply button payloads.
    if text == "#feedback_up":
        logger.info(f"User {user_id} gave 👍 feedback via Zalo")
        zalo_api.send_text_message(user_id, "Cảm ơn bạn đã đánh giá! Phản hồi của bạn giúp tôi học hỏi tốt hơn.")
        return
    if text == "#feedback_down":
        logger.info(f"User {user_id} gave 👎 feedback via Zalo")
        zalo_api.send_text_message(user_id, "Cảm ơn bạn đã góp ý. Tôi sẽ ghi nhận để nhóm phát triển cải thiện.")
        return
    if text == "#human_handover":
        chat_db.flag_needs_human(f"zalo_{user_id}")
        zalo_api.send_text_message(user_id, "Tôi đã chuyển yêu cầu của bạn đến thầy cô tư vấn viên. Vui lòng đợi trong giây lát.")
        return

    if chat_db.is_user_blocked(user_id):
        logger.info(f"Ignored message from blocked Zalo user {user_id}")
        return

    try:
        check_rate_limit(f"zalo_{user_id}")
    except Exception:
        logger.warning(f"Rate limit exceeded for Zalo user {user_id}")
        return

    chat_db.log_message(user_id, "user", text)

    # Last few turns for context. Drop the just-logged current message ([:-1]),
    # then keep the most recent 6 records.
    history_records = chat_db.get_chat_history(user_id)[:-1][-6:]
    history = [{"role": r["role"], "content": r["content"]} for r in history_records]

    final_response = ""
    for current_text in chat_response(text, history):
        final_response = current_text

    chat_db.log_message(user_id, "assistant", final_response)
    logger.info(f"Sending interactive response to Zalo user {user_id}: {final_response[:100]}...")

    if response_needs_human(final_response):
        chat_db.flag_needs_human(f"zalo_{user_id}")
        zalo_api.send_text_message(user_id, final_response)
    else:
        buttons = [
            {"title": "👍 Hữu ích", "type": "oa.query.hide", "payload": "#feedback_up"},
            {"title": "👎 Chưa đúng", "type": "oa.query.hide", "payload": "#feedback_down"},
            {"title": "Tư vấn viên", "type": "oa.query.hide", "payload": "#human_handover"}
        ]
        zalo_api.send_interactive_message(user_id, final_response, buttons)


@router.post("/zalo/webhook")
async def zalo_webhook(req: Request):
    try:
        raw_body = (await req.body()).decode("utf-8")
        data = json.loads(raw_body) if raw_body else {}

        # Verify the request actually came from Zalo before doing any work.
        if not zalo_api.verify_signature(
            app_id=data.get("app_id", ""),
            raw_body=raw_body,
            timestamp=str(data.get("timestamp", "")),
            signature=req.headers.get("X-ZEvent-Signature", ""),
        ):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

        event_name = data.get("event_name")
        sender = data.get("sender", {})
        message = data.get("message", {})
        logger.info(f"Zalo webhook received event: {event_name}")

        if event_name == "user_send_text":
            user_id = sender.get("id")
            text = message.get("text", "")
            logger.info(f"Zalo user message from {user_id}: {text[:100]}...")
            if user_id and text:
                # Offload blocking I/O + LLM call so the event loop isn't stalled.
                await run_in_threadpool(_process_user_text, user_id, text)

        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Zalo Webhook: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/api/admin/conversations")
async def get_conversations(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "conversations": chat_db.get_conversations()}

@router.get("/api/admin/conversations/blocked")
async def get_blocked_list(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "blocked_users": chat_db.get_blocked_users()}

@router.get("/api/admin/conversations/{user_id}")
async def get_conversation_history(user_id: str, current_user: dict = Depends(get_current_user)):
    return {"status": "success", "history": chat_db.get_chat_history(user_id)}

class ManualReplyRequest(BaseModel):
    message: str

@router.post("/api/admin/conversations/{user_id}/reply")
async def send_manual_reply(user_id: str, req: ManualReplyRequest, current_user: dict = Depends(get_current_user)):
    success = zalo_api.send_text_message(user_id, req.message)
    if success:
        chat_db.log_message(user_id, "admin", req.message)
        chat_db.clear_human_flag(user_id)
        return {"status": "success"}
    return {"status": "error", "message": "Failed to send message"}

class BlockUserRequest(BaseModel):
    reason: str = ""

@router.post("/api/admin/conversations/{user_id}/block")
async def block_zalo_user(user_id: str, req: BlockUserRequest, current_user: dict = Depends(get_current_user)):
    chat_db.block_user(user_id, req.reason)
    logger.info(f"AUDIT: Admin {current_user['username']} blocked Zalo user {user_id}. Reason: {req.reason}")
    return {"status": "success", "message": f"User {user_id} has been blocked."}

@router.post("/api/admin/conversations/{user_id}/unblock")
async def unblock_zalo_user(user_id: str, current_user: dict = Depends(get_current_user)):
    chat_db.unblock_user(user_id)
    logger.info(f"AUDIT: Admin {current_user['username']} unblocked Zalo user {user_id}.")
    return {"status": "success", "message": f"User {user_id} has been unblocked."}
