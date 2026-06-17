import logging
from src.core.multimodal import MultimodalEngine
from src.core.vector_db import VectorDBManager
from src.config.settings import settings

logger = logging.getLogger(__name__)

# Initialize core components
engine = MultimodalEngine()
db_manager = VectorDBManager()

def chat_response(message, history):
    """
    Core RAG + Gemini chat response logic.
    """
    # Robustly normalize message to string
    def extract_text(m):
        if isinstance(m, str):
            return m
        if isinstance(m, dict):
            return extract_text(m.get("text", m.get("content", str(m))))
        if isinstance(m, (list, tuple)):
            return extract_text(m[0]) if m else ""
        return str(m)
        
    message = extract_text(message)
        
    yield '🔍 Đang tra cứu tài liệu<span class="searching-dots"><span>.</span><span>.</span><span>.</span></span>'
    
    # 1. Retrieval
    db = db_manager.get_db()
    context = ""
    chatbot_prompts = settings.PROMPTS.get("chatbot", {})
    
    # Skip retrieval for very short messages or simple greetings
    greetings = ["chào", "hi", "hello", "xin chào", "hey", "chao"]
    is_greeting = message.lower().strip() in greetings
    
    if db and len(message.strip()) > 10 and not is_greeting:
        docs = db.similarity_search(message, k=3)
        prefix = chatbot_prompts.get("context_prefix", "Thông tin tham khảo:")
        context = f"\n\n{prefix}\n" + "\n".join([d.page_content for d in docs])
    
    # 2. Multimodal Query
    template = chatbot_prompts.get("query_template", "{context}\n\n{message}")
    prompt = template.format(context=context, message=message)
    
    try:
        full_response = ""
        for chunk in engine.query_stream([], prompt):
            full_response += chunk
            yield full_response
    except Exception as e:
        logger.exception("Error in chatbot")
        yield f"Lỗi hệ thống: {str(e)}"
