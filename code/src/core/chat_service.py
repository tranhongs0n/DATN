import logging
from src.core.multimodal import MultimodalEngine
from src.core.vector_db import VectorDBManager
from src.core.semantic_cache import SemanticCache
from src.config.settings import settings



logger = logging.getLogger(__name__)

engine = MultimodalEngine()
db_manager = VectorDBManager()
semantic_cache = SemanticCache(similarity_threshold=0.96)

# Markers signalling the bot could not answer / asked the user to wait.
# Centralized so callers (e.g. Zalo handover) don't hard-code prose strings.
NO_ANSWER_MARKER = "Xin lỗi, tôi không thể tìm thấy"
HANDOVER_MARKERS = (NO_ANSWER_MARKER, "Vui lòng đợi")


def response_needs_human(text: str) -> bool:
    """True if a bot response should be escalated to a human advisor."""
    return any(m in text for m in HANDOVER_MARKERS)

def chat_response(message, history):
    """
    Core RAG + Gemini chat response logic.
    """
    def extract_text(m):
        if isinstance(m, str):
            return m
        if isinstance(m, dict):
            return extract_text(m.get("text", m.get("content", str(m))))
        if isinstance(m, (list, tuple)):
            return extract_text(m[0]) if m else ""
        return str(m)
        
    message = extract_text(message)
    
    greetings = ["chào", "hi", "hello", "xin chào", "hey", "chao"]
    is_greeting = message.lower().strip() in greetings
    
    if is_greeting or len(message.strip()) < 10:
        yield "Chào bạn! Tôi là Trợ lý Tuyển sinh của Trường Đại học Thủy lợi. Tôi có thể giúp gì cho bạn hôm nay?"
        return
        
    if not history:
        cached_answer = semantic_cache.get_cached_response(message)
        if cached_answer:
            yield cached_answer
            return

    yield '🔍 Đang tra cứu tài liệu<span class="searching-dots"><span>.</span><span>.</span><span>.</span></span>'
    
    history_context = ""
    if history:
        parts = []
        for msg in history:
            role = msg.get("role", "")
            content = extract_text(msg.get("content", ""))
            if role == "user":
                parts.append(f"Human: {content}")
            elif role == "assistant":
                parts.append(f"AI: {content}")
        history_context = "\n".join(parts)
    
    db = db_manager.get_db()
    bm25 = db_manager.get_bm25_retriever()
    context = ""
    chatbot_prompts = settings.PROMPTS.get("chatbot", {})
    
    if db:
        chroma_retriever = db.as_retriever(search_kwargs={"k": 3})
        if bm25:
            bm25.k = 3
            docs_bm25 = bm25.invoke(message)
            docs_chroma = chroma_retriever.invoke(message)
            
            doc_scores = {}
            for rank, doc in enumerate(docs_bm25):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.4 / (rank + 60)
            for rank, doc in enumerate(docs_chroma):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.6 / (rank + 60)
                
            all_docs = {doc.page_content: doc for doc in docs_bm25 + docs_chroma}
            docs = [all_docs[content] for content, _ in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)]
            docs = docs[:4]
        else:
            docs = chroma_retriever.invoke(message)
            
        prefix = chatbot_prompts.get("context_prefix", "Thông tin tham khảo:")
        
        import os
        from datetime import datetime
        current_year = datetime.now().year
        context_parts = [f"THÔNG TIN HỆ THỐNG: Năm hiện tại là {current_year}. Hãy dùng thông tin này để hiểu các từ như 'năm nay', 'năm ngoái', 'năm sau' trong câu hỏi của người dùng.\n"]
        
        for d in docs:
            source = d.metadata.get("source", "Không rõ nguồn") if d.metadata else "Không rõ nguồn"
            filename = os.path.basename(source)
            context_parts.append(f"[Nguồn: {filename}]\n{d.page_content}")
            
        context = f"\n\n{prefix}\n" + "\n---\n".join(context_parts)
    
    if history_context:
        context = f"Lịch sử hội thoại:\n{history_context}\n{context}"
        
    template = chatbot_prompts.get("query_template", "{context}\n\n{message}")
    template += "\n\nHƯỚNG DẪN QUAN TRỌNG 1: Nếu câu hỏi thiếu ngữ cảnh cụ thể (ví dụ: hỏi điểm chuẩn/học phí nhưng không nói rõ NGÀNH HỌC hoặc NĂM HỌC nào), hãy lịch sự hỏi lại người dùng để họ bổ sung thông tin thay vì đoán bừa."
    template += "\n\nHƯỚNG DẪN QUAN TRỌNG 2: Nếu bạn tìm thấy câu trả lời, bạn BẮT BUỘC phải trích dẫn tên tệp tài liệu ở cuối (VD: Nguồn tham khảo: De_an_tuyen_sinh_2024.pdf) dựa trên thông tin [Nguồn: ...] được cung cấp."
    prompt = template.format(context=context, message=message)
    
    try:
        full_response = ""
        for chunk in engine.query_stream([], prompt):
            full_response += chunk
            yield full_response
            
        if not history and full_response and NO_ANSWER_MARKER not in full_response:
            semantic_cache.set_cached_response(message, full_response)
            
    except Exception as e:
        logger.exception("Error in chatbot")
        yield f"Lỗi hệ thống: {str(e)}"
