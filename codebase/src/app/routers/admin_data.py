from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import os
import shutil
import sqlite3

from src.config.settings import settings
from src.core import chat_db
from src.core.chat_service import db_manager
from src.app.dependencies import get_current_user, logger, indexing_service, loader

router = APIRouter(prefix="/api/admin", tags=["admin_data"])

@router.get("/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    stats = db_manager.get_stats()
    return {
        "doc_count": stats["doc_count"],
        "chunk_count": stats["chunk_count"],
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "llm_model": settings.GEMINI_MODEL_NAME
    }

@router.get("/files")
async def get_files(current_user: dict = Depends(get_current_user)):
    file_data, choices = indexing_service.get_file_status_list()
    return {"files": [{"name": f[0], "status": f[1], "path": str(f[2])} for f in file_data]}

@router.get("/files/unsupported")
async def get_unsupported_files(current_user: dict = Depends(get_current_user)):
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

@router.delete("/files/{filename}")
def delete_file(filename: str, current_user: dict = Depends(get_current_user)):
    path_map = indexing_service.get_full_path_map()
    file_path = path_map.get(filename)
    if not file_path or not os.path.exists(file_path):
        return {"status": "error", "message": "File không tồn tại."}
        
    try:
        os.remove(file_path)

        try:
            db = db_manager.get_db()
            if db:
                db.delete(where={"source": file_path})
        except Exception as e:
            logger.warning(f"Failed to remove {filename} from vector db: {e}")
            
        return {"status": "success", "message": f"Đã xóa file {filename} thành công."}
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")
        return {"status": "error", "message": f"Lỗi khi xóa file: {str(e)}"}

class ConvertRequest(BaseModel):
    filename: str

@router.post("/files/convert")
def convert_file(req: ConvertRequest, current_user: dict = Depends(get_current_user)):
    from src.core.chat_service import engine
    try:
        new_filename = indexing_service.convert_unsupported_file(req.filename, engine)
        return {"status": "success", "message": f"Đã chuyển đổi thành công: {new_filename}", "new_file": new_filename}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi chuyển đổi: {str(e)}"}

@router.post("/files/convert-all")
def convert_all_files(current_user: dict = Depends(get_current_user)):
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
            
    return {"status": "success", "message": f"Chuyển đổi hoàn tất: {converted} thành công, {errors} lỗi."}

@router.post("/index/rebuild")
def rebuild_index(current_user: dict = Depends(get_current_user)):
    logger.info(f"AUDIT: User {current_user['username']} triggered full index rebuild")
    docs = indexing_service.load_all_from_disk()
    if not docs:
        logger.warning("No documents found to index during rebuild")
        return {"status": "error", "message": "Không tìm thấy tài liệu nào để index."}
    try:
        db_manager.build_from_documents(docs)
        logger.info(f"Successfully rebuilt index with {len(docs)} documents")
        return {"status": "success", "message": f"Hoàn thành xây dựng Index với {len(docs)} tài liệu!"}
    except Exception as e:
        logger.error(f"Error rebuilding index: {e}")
        return {"status": "error", "message": f"Lỗi API hoặc VectorDB: {str(e)}"}

@router.post("/index/upload")
def index_upload(files: List[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    if not files:
        return {"status": "error", "message": "Không có tệp nào để xử lý."}
    
    file_names = [f.filename for f in files]
    logger.info(f"Admin uploaded files for indexing: {file_names}")
    
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
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản."}
        
    try:
        db_manager.build_from_documents(docs, append=True)
        return {"status": "success", "message": f"Đã cập nhật Database thành công với {len(docs)} đoạn!"}
    except Exception as e:
        logger.error(f"Error indexing upload: {e}")
        return {"status": "error", "message": f"Lỗi API hoặc VectorDB: {str(e)}"}

class SelectedFilesRequest(BaseModel):
    files: List[str]

@router.post("/index/selected")
def index_selected(req: SelectedFilesRequest, current_user: dict = Depends(get_current_user)):
    if not req.files:
        return {"status": "error", "message": "Vui lòng chọn ít nhất một tệp."}
        
    path_map = indexing_service.get_full_path_map()
    file_paths = [path_map.get(name) for name in req.files if path_map.get(name)]
    docs = indexing_service.load_files_by_path(file_paths)
    
    if not docs:
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản từ các tệp đã chọn."}
        
    try:
        db_manager.build_from_documents(docs, append=True)
        return {"status": "success", "message": f"Hoàn thành! Đã index {len(req.files)} tệp."}
    except Exception as e:
        logger.error(f"Error indexing selected files: {e}")
        return {"status": "error", "message": f"Lỗi API hoặc VectorDB: {str(e)}"}

@router.get("/export/chats")
def export_chats(current_user: dict = Depends(get_current_user)):
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

@router.get("/export/documents")
def export_documents(current_user: dict = Depends(get_current_user)):
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

class AbbreviationRequest(BaseModel):
    short_form: str
    full_form: str

@router.get("/abbreviations")
def get_abbreviations(current_user: dict = Depends(get_current_user)):
    return {"abbreviations": chat_db.get_all_abbreviations()}

@router.post("/abbreviations")
def create_abbreviation(req: AbbreviationRequest, current_user: dict = Depends(get_current_user)):
    from src.core.chat_service import reload_abbreviations
    chat_db.add_abbreviation(req.short_form, req.full_form)
    reload_abbreviations()
    return {"status": "success", "message": "Thêm từ viết tắt thành công."}

@router.put("/abbreviations/{abbr_id}")
def update_abbreviation_api(abbr_id: int, req: AbbreviationRequest, current_user: dict = Depends(get_current_user)):
    from src.core.chat_service import reload_abbreviations
    chat_db.update_abbreviation(abbr_id, req.short_form, req.full_form)
    reload_abbreviations()
    return {"status": "success", "message": "Cập nhật từ viết tắt thành công."}

@router.delete("/abbreviations/{abbr_id}")
def delete_abbreviation_api(abbr_id: int, current_user: dict = Depends(get_current_user)):
    from src.core.chat_service import reload_abbreviations
    chat_db.delete_abbreviation(abbr_id)
    reload_abbreviations()
    return {"status": "success", "message": "Xóa từ viết tắt thành công."}

@router.post("/abbreviations/import")
def import_abbreviations(data: dict, current_user: dict = Depends(get_current_user)):
    from src.core.chat_service import reload_abbreviations
    try:
        count = 0
        for k, v in data.items():
            if not isinstance(k, str) or not isinstance(v, str): continue
            chat_db.add_abbreviation(k, v)
            count += 1
        reload_abbreviations()
        return {"status": "success", "message": f"Import thành công {count} từ viết tắt."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi xử lý dữ liệu: {str(e)}"}

@router.get("/test_retrieval")
async def test_retrieval(query: str, current_user: str = Depends(get_current_user)):
    from src.core.vector_db import VectorDBManager
    db_manager = VectorDBManager()
    chroma_db = db_manager.get_db()
    bm25 = db_manager.get_bm25_retriever()
    
    if not chroma_db:
        return {"results": []}
        
    try:
        chroma_retriever = chroma_db.as_retriever(search_kwargs={"k": 4})
        
        if bm25:
            bm25.k = 3
            docs_bm25 = bm25.invoke(query)
            docs_chroma = chroma_retriever.invoke(query)
            
            doc_scores = {}
            for rank, doc in enumerate(docs_bm25):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.4 / (rank + 60)
            for rank, doc in enumerate(docs_chroma):
                doc_scores[doc.page_content] = doc_scores.get(doc.page_content, 0) + 0.6 / (rank + 60)
                
            all_docs = {doc.page_content: doc for doc in docs_bm25 + docs_chroma}
            sorted_items = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
            
            results = []
            for content, score in sorted_items[:5]:
                doc = all_docs[content]
                source = os.path.basename(doc.metadata.get("source", "Không rõ")) if doc.metadata else "Không rõ"
                results.append({
                    "content": content,
                    "source": source,
                    "score": score
                })
            return {"results": results}
        else:
            docs = chroma_retriever.invoke(query)
            results = []
            for doc in docs:
                source = os.path.basename(doc.metadata.get("source", "Không rõ")) if doc.metadata else "Không rõ"
                results.append({
                    "content": doc.page_content,
                    "source": source,
                    "score": 1.0
                })
            return {"results": results}
            
    except Exception as e:
        import logging
        logging.error(f"Error in test_retrieval: {e}")
        return {"results": []}



@router.post("/api/docs")
def index_upload_docs_alias(files: List[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    return index_upload(files, current_user)

@router.get("/api/logs")
def get_logs_alias(current_user: dict = Depends(get_current_user)):
    import sqlite3
    from src.core.chat_db import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT log_id, session_id, user_query, bot_response, latency_ms, timestamp FROM CHAT_LOG ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()
        logs = [{"log_id": r[0], "session_id": r[1], "user_query": r[2], "bot_response": r[3], "latency_ms": r[4], "timestamp": r[5]} for r in rows]
    except Exception as e:
        logs = []
    conn.close()
    return {"status": "success", "logs": logs}
