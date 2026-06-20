from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import shutil
from typing import List, Dict, Any

from src.core.chat_service import chat_response, db_manager
from src.core.indexing import IndexingService
from src.utils.document_loader import DocumentLoader
from src.config.settings import settings

app = FastAPI(title="DATN RAG API")

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

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    def event_generator():
        try:
            for response_text in chat_response(req.message, req.history):
                # We yield the full text at each step
                data = json.dumps({"text": response_text})
                yield f"data: {data}\n\n"
            yield f"data: [DONE]\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"
            yield f"data: [DONE]\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/admin/stats")
async def get_stats():
    stats = db_manager.get_stats()
    return {
        "doc_count": stats["doc_count"],
        "chunk_count": stats["chunk_count"],
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "llm_model": settings.GEMINI_MODEL_NAME
    }

@app.get("/api/admin/files")
async def get_files():
    file_data, choices = indexing_service.get_file_status_list()
    # file_data is a list of [basename, status, filepath]
    return {"files": [{"name": f[0], "status": f[1], "path": str(f[2])} for f in file_data]}

@app.post("/api/admin/index/rebuild")
async def rebuild_index():
    docs = indexing_service.load_all_from_disk()
    if not docs:
        return {"status": "error", "message": "Không tìm thấy tài liệu nào để index."}
    db_manager.build_from_documents(docs)
    return {"status": "success", "message": f"Hoàn thành xây dựng Index với {len(docs)} tài liệu!"}

@app.post("/api/admin/index/upload")
async def index_upload(files: List[UploadFile] = File(...)):
    if not files:
        return {"status": "error", "message": "Không có tệp nào để xử lý."}
    
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
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản."}
        
    db_manager.build_from_documents(docs, append=True)
    return {"status": "success", "message": f"Đã cập nhật Database thành công với {len(docs)} đoạn!"}

class SelectedFilesRequest(BaseModel):
    files: List[str]

@app.post("/api/admin/index/selected")
async def index_selected(req: SelectedFilesRequest):
    if not req.files:
        return {"status": "error", "message": "Vui lòng chọn ít nhất một tệp."}
        
    path_map = indexing_service.get_full_path_map()
    file_paths = [path_map.get(name) for name in req.files if path_map.get(name)]
    docs = indexing_service.load_files_by_path(file_paths)
    
    if not docs:
        return {"status": "error", "message": "Lỗi: Không thể trích xuất văn bản từ các tệp đã chọn."}
        
    db_manager.build_from_documents(docs, append=True)
    return {"status": "success", "message": f"Hoàn thành! Đã index {len(req.files)} tệp."}

@app.get("/api/admin/files/unsupported")
async def get_unsupported_files():
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
async def convert_file(req: ConvertRequest):
    """Converts an unsupported file to .docx via AI."""
    from src.core.chat_service import engine
    try:
        new_filename = indexing_service.convert_unsupported_file(req.filename, engine)
        return {"status": "success", "message": f"Đã chuyển đổi thành công: {new_filename}", "new_file": new_filename}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi chuyển đổi: {str(e)}"}

@app.post("/api/admin/scrape")
async def start_scrape(category: str = Form("all"), limit: int = Form(10)):
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
            
        return {"status": "success", "message": "Hoàn thành quá trình Scraping!"}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi Scraping: {str(e)}"}

@app.post("/api/admin/files/convert-all")
async def convert_all_files():
    """Bulk converts all unsupported files to .docx."""
    from src.core.chat_service import engine
    
    # Discovery
    all_files = loader.get_available_files(include_assets=True)
    unsupported = [os.path.basename(f) for f in all_files if not f.lower().endswith(('.pdf', '.docx'))]
    
    if not unsupported:
        return {"status": "success", "message": "Không có tệp nào cần chuyển đổi."}
        
    converted_count = 0
    errors = []
    
    for filename in unsupported:
        try:
            indexing_service.convert_unsupported_file(filename, engine)
            converted_count += 1
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
            
    if errors:
        return {
            "status": "warning", 
            "message": f"Đã chuyển đổi {converted_count} tệp, nhưng có {len(errors)} lỗi.",
            "errors": errors
        }
        
    return {"status": "success", "message": f"Đã chuyển đổi thành công tất cả {converted_count} tệp!"}

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
