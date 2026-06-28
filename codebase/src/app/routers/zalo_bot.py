from fastapi import APIRouter, Request, HTTPException
from fastapi.concurrency import run_in_threadpool
import json

from src.core.chat_service import chat_response
from src.core import chat_db
from src.app.dependencies import zalo_bot, logger, check_rate_limit

router = APIRouter(tags=["zalo_bot"])


def _process_message(chat_id: str, text: str):
    try:
        check_rate_limit(f"zalobot_{chat_id}")
    except Exception:
        logger.warning(f"Rate limit exceeded for Zalo Bot chat {chat_id}")
        return

    history_records = chat_db.get_chat_history(chat_id)[-6:]
    history = [{"role": r["role"], "content": r["content"]} for r in history_records]

    import time
    start_time = time.time()
    final_response = ""
    for current_text in chat_response(text, history, is_zalo=True):
        final_response = current_text
    latency = (time.time() - start_time) * 1000

    chat_db.log_chat_interaction(chat_id, text, final_response, latency_ms=latency)
    logger.info(f"Sending Zalo Bot response to {chat_id}: {final_response[:100]}...")
    zalo_bot.send_message(chat_id, final_response)


@router.post("/api/webhook")
@router.post("/zalo/bot/webhook")
async def zalo_bot_webhook(req: Request):
    try:
        if not zalo_bot.verify_secret(req.headers.get("X-Bot-Api-Secret-Token", "")):
            raise HTTPException(status_code=401, detail="Invalid webhook secret")

        raw_body = (await req.body()).decode("utf-8")
        data = json.loads(raw_body) if raw_body else {}

        event_name = data.get("event_name")
        message_data = data.get("message", {})
        
        logger.info(f"Zalo Bot webhook received event: {event_name}")

        if event_name == "message.text.received":
            chat_id = message_data.get("chat", {}).get("id") or message_data.get("from", {}).get("id")
            text = message_data.get("text", "")
            if chat_id and text:
                await run_in_threadpool(_process_message, chat_id, text)

        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Zalo Bot Webhook: {e}")
        return {"ok": False, "error": str(e)}
