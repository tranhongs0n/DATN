from fastapi import APIRouter, Depends, UploadFile, File, Form
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
        # Also remove from vector db if it's indexed
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
