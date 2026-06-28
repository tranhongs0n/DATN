import time
from src.utils.zalo_bot import ZaloBot
from src.core.chat_service import chat_response
from src.core import chat_db
from src.utils.logger_setup import setup_logger

logger = setup_logger("DATN-ZaloPolling")
zalo_bot = ZaloBot()

def _process_message(chat_id: str, text: str):
    try:
        chat_db.log_message(chat_id, "user", text)
        
        history_records = chat_db.get_chat_history(chat_id)[:-1][-6:]
        history = [{"role": r["role"], "content": r["content"]} for r in history_records]

        final_response = ""
        for current_text in chat_response(text, history, is_zalo=True):
            final_response = current_text

        chat_db.log_message(chat_id, "assistant", final_response)
        logger.info(f"Sending response to {chat_id}: {final_response[:100]}...")
        zalo_bot.send_message(chat_id, final_response)
    except Exception as e:
        logger.error(f"Error processing message from {chat_id}: {e}")

def start_polling():
    logger.info("Starting Zalo Bot Polling (Long Polling)...")
    offset = None
    
    if not zalo_bot.token:
        logger.error("ZALO_BOT_TOKEN is not set in environment. Polling will stop.")
        return

    while True:
        try:
            updates = zalo_bot.get_updates(offset=offset, timeout=30)
            for update in updates:
                update_id = update.get("update_id")
                if update_id is not None:
                    offset = update_id + 1
                
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id") or message.get("from", {}).get("id")
                text = message.get("text", "")
                
                if chat_id and text:
                    logger.info(f"Received message from {chat_id}: {text}")
                    _process_message(str(chat_id), text)
        except Exception as e:
            logger.error(f"Polling loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_polling()
