import sqlite3
import json
import time
import os
import logging
import numpy as np
from src.core.vector_db import GeminiEmbeddings
from src.config.settings import settings

logger = logging.getLogger(__name__)

CACHE_DB_PATH = os.path.join(settings.DATA_DIR, "semantic_cache.db")
CACHE_MAX_ROWS = 1000
CACHE_TTL_SECONDS = 30 * 24 * 3600

def init_cache_db():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS semantic_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            embedding_json TEXT NOT NULL,
            response_text TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class SemanticCache:
    def __init__(self, similarity_threshold=0.96):
        init_cache_db()
        self.embeddings_model = GeminiEmbeddings()
        self.similarity_threshold = similarity_threshold

    def embed(self, query_text: str):
        return self.embeddings_model.embed_query(query_text)

    def get_cached_response(self, query_text: str, query_emb=None) -> str:
        try:
            if query_emb is None:
                query_emb = self.embed(query_text)

            conn = sqlite3.connect(CACHE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT embedding_json, response_text FROM semantic_cache")
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                return None

            q = np.asarray(query_emb, dtype=np.float32)
            q_norm = np.linalg.norm(q)
            if q_norm == 0:
                return None

            matrix = np.asarray([json.loads(r[0]) for r in rows], dtype=np.float32)
            norms = np.linalg.norm(matrix, axis=1)
            valid = norms > 0
            if not valid.any():
                return None

            sims = np.zeros(len(rows), dtype=np.float32)
            sims[valid] = (matrix[valid] @ q) / (norms[valid] * q_norm)

            best_idx = int(np.argmax(sims))
            highest_sim = float(sims[best_idx])

            if highest_sim >= self.similarity_threshold:
                logger.info(f"CACHE HIT (Sim: {highest_sim:.3f}): '{query_text}'")
                return rows[best_idx][1]

            return None
        except Exception as e:
            logger.error(f"Semantic Cache Error (get): {e}")
            return None

    def set_cached_response(self, query_text: str, response_text: str, query_emb=None):
        try:
            if query_emb is None:
                query_emb = self.embed(query_text)
            emb_json = json.dumps(query_emb)

            conn = sqlite3.connect(CACHE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO semantic_cache (query_text, embedding_json, response_text, created_at)
                VALUES (?, ?, ?, ?)
            ''', (query_text, emb_json, response_text, time.time()))
            cursor.execute("DELETE FROM semantic_cache WHERE created_at < ?", (time.time() - CACHE_TTL_SECONDS,))
            cursor.execute('''
                DELETE FROM semantic_cache WHERE id NOT IN (
                    SELECT id FROM semantic_cache ORDER BY created_at DESC LIMIT ?
                )
            ''', (CACHE_MAX_ROWS,))
            conn.commit()
            conn.close()
            logger.info(f"Stored query in semantic cache: '{query_text[:50]}...'")
        except Exception as e:
            logger.error(f"Semantic Cache Error (set): {e}")
