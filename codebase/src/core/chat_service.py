import logging
from src.core.multimodal import MultimodalEngine
from src.core.vector_db import VectorDBManager
from src.core.semantic_cache import SemanticCache
from src.config.settings import settings



logger = logging.getLogger(__name__)

engine = MultimodalEngine()
db_manager = VectorDBManager()
semantic_cache = SemanticCache(similarity_threshold=0.96)

from src.core import chat_db

ABBREVIATIONS = {}

def reload_abbreviations():
    global ABBREVIATIONS
    try:
        abbrs = chat_db.get_all_abbreviations()
        ABBREVIATIONS = {a["short_form"]: a["full_form"] for a in abbrs}
    except Exception as e:
        logger.error(f"Error loading abbreviations: {e}")

reload_abbreviations()

def expand_abbreviations(text: str) -> str:
    import re
    words = re.split(r'(\W+)', text)
    expanded = [ABBREVIATIONS.get(w.lower(), w) for w in words]
    return "".join(expanded)

NO_ANSWER_MARKER = "Xin lỗi, tôi không thể tìm thấy"
HANDOVER_MARKERS = (NO_ANSWER_MARKER, "Vui lòng đợi")


def response_needs_human(text: str) -> bool:
    return any(m in text for m in HANDOVER_MARKERS)

def chat_response(message, history, is_zalo=False):
    def extract_text(m):
        if isinstance(m, str):
            return m
        if isinstance(m, dict):
            return extract_text(m.get("text", m.get("content", str(m))))
        if isinstance(m, (list, tuple)):
            return extract_text(m[0]) if m else ""
        return str(m)
        
    message = extract_text(message)
    message = expand_abbreviations(message)
    
    query_emb = None
    if not history:
        query_emb = semantic_cache.embed(message)
        cached_answer = semantic_cache.get_cached_response(message, query_emb=query_emb)
        if cached_answer:
            yield cached_answer
            return

    if not is_zalo:
        yield '🔍 Đang tra cứu tài liệu<span class="searching-dots"><span>.</span><span>.</span><span>.</span></span>'
    
    history_context = ""
    if history:
        try:
            from langchain.memory import ConversationBufferMemory
            memory = ConversationBufferMemory()
            for msg in history:
                role = msg.get("role", "")
                content = extract_text(msg.get("content", ""))
                if role == "user":
                    memory.chat_memory.add_user_message(content)
                elif role == "assistant":
                    memory.chat_memory.add_ai_message(content)
            history_context = memory.buffer
        except ImportError:
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
    
    search_query = message
    if history:
        for msg in reversed(history):
            if msg.get("role") == "user":
                last_human = extract_text(msg.get("content", ""))
                if last_human.strip().lower() != message.strip().lower():
                    search_query = f"{last_human} {message}"
                break
    
    if db:
        chroma_retriever = db.as_retriever(search_kwargs={"k": 3})
        if bm25:
            bm25.k = 3
            docs_bm25 = bm25.invoke(search_query)
            docs_chroma = chroma_retriever.invoke(search_query)
            
            doc_scores = {}
            for rank, doc in enumerate(docs_bm25):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.4 / (rank + 60)
            for rank, doc in enumerate(docs_chroma):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.6 / (rank + 60)
                
            all_docs = {doc.page_content: doc for doc in docs_bm25 + docs_chroma}
            docs = [all_docs[content] for content, _ in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)]
            docs = docs[:4]
        else:
            docs = chroma_retriever.invoke(search_query)
            
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
    template += "\n\nHƯỚNG DẪN QUAN TRỌNG 1: LUÔN sử dụng 'Lịch sử hội thoại' để xác định Chủ đề/Ngành học/Năm học nếu câu hỏi hiện tại bị thiếu. NẾU KHÔNG TÌM THẤY THÔNG TIN TRONG TÀI LIỆU, hãy trả lời rõ: 'Hệ thống chưa có thông tin <Chủ đề lấy từ Lịch sử>'. TUYỆT ĐỐI KHÔNG yêu cầu người dùng cung cấp lại ngành học nếu nó đã có trong Lịch sử."
    if not is_zalo:
        template += "\n\nHƯỚNG DẪN QUAN TRỌNG 2: Nếu bạn tìm thấy câu trả lời, bạn BẮT BUỘC phải trích dẫn tên tệp tài liệu ở cuối (VD: Nguồn tham khảo: De_an_tuyen_sinh_2024.pdf) dựa trên thông tin [Nguồn: ...] được cung cấp."
    template += "\n\nHƯỚNG DẪN QUAN TRỌNG 3: Khi trả lời về Điểm chuẩn, Học phí, hoặc Chỉ tiêu, BẮT BUỘC phải nói rõ là CỦA NĂM NÀO (dựa theo tiêu đề tệp hoặc nội dung). Nếu tài liệu không có năm, phải ghi chú: 'Tài liệu không ghi rõ năm áp dụng'."
    template += "\n\nHƯỚNG DẪN QUAN TRỌNG 4: TUYỆT ĐỐI KHÔNG trộn lẫn thông tin giữa các Bậc đào tạo (Đại học, Thạc sĩ, Tiến sĩ/Nghiên cứu sinh). Nếu câu hỏi không ghi rõ hệ nào, BẮT BUỘC ưu tiên trả lời thông tin hệ ĐẠI HỌC (chính quy) lên đầu tiên, sau đó mới liệt kê riêng biệt các hệ khác nếu có."
    
    if is_zalo:
        template += "\n\nHƯỚNG DẪN QUAN TRỌNG 5: TRẢ LỜI CHO ZALO. TUYỆT ĐỐI KHÔNG SỬ DỤNG ĐỊNH DẠNG MARKDOWN (không dùng in đậm **, in nghiêng *, danh sách # hay -, hay code block). KHÔNG BAO GIỜ thêm 'Nguồn tham khảo' ở cuối câu trả lời. Chỉ viết chữ text thuần tuý, dùng gạch ngang hoặc số để liệt kê."
        
    prompt = template.format(context=context, message=message)
    
    try:
        full_response = ""
        for chunk in engine.query_stream([], prompt):
            full_response += chunk
            yield full_response
            
        if not history and full_response and NO_ANSWER_MARKER not in full_response:
            semantic_cache.set_cached_response(message, full_response, query_emb=query_emb)
            
    except Exception as e:
        logger.exception("Error in chatbot")
        yield f"Lỗi hệ thống: {str(e)}"
