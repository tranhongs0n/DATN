from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from src.app.routers import auth, admin_users, chat, zalo, admin_data, admin_scrape
from src.core import auth as auth_core
from src.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the auth DB at startup instead of at import time.
    auth_core.init_db()
    yield


app = FastAPI(title="DATN RAG API", lifespan=lifespan)

# Origins allowed for CORS. Override via ALLOWED_ORIGINS env (comma-separated).
# Note: "*" with allow_credentials=True is rejected by browsers, so we list explicit origins.
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
app.include_router(zalo.router)
app.include_router(admin_data.router)
app.include_router(admin_scrape.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "vector_db": "connected", "api": "running"}

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
