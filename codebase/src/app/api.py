from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from src.app.routers import auth, admin_users, chat, admin_data, admin_scrape, zalo_bot
from src.core import auth as auth_core
from src.core import chat_db
from src.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    auth_core.init_db()
    chat_db.init_db()
    yield


app = FastAPI(title="DATN RAG API", lifespan=lifespan)

allowed_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()] or [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin_users.router)
app.include_router(chat.router)
app.include_router(zalo_bot.router)
app.include_router(admin_data.router)
app.include_router(admin_scrape.router)

@app.get("/health")
def health_check():
    from src.core.chat_service import db_manager
    try:
        stats = db_manager.get_stats()
        vector_db = "connected" if stats["chunk_count"] > 0 else "empty"
    except Exception:
        vector_db = "error"
    status = "ok" if vector_db != "error" else "degraded"
    return {"status": status, "vector_db": vector_db, "api": "running"}

@app.get("/")
def read_index():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(app_dir, "static/index.html"))

@app.get("/admin")
def read_admin():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(app_dir, "static/admin.html"))

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
