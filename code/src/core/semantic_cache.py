import sqlite3
import json
import math
import time
import os
import logging
from src.core.vector_db import GeminiEmbeddings
from src.config.settings import settings

logger = logging.getLogger(__name__)

CACHE_DB_PATH = os.path.join(settings.DATA_DIR, "semantic_cache.db")

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

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        return 0.0
    dot_product = sum(x * y for x, y in zip(v1, v2))
    norm_v1 = math.sqrt(sum(x * x for x in v1))
    norm_v2 = math.sqrt(sum(y * y for y in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

class SemanticCache:
    def __init__(self, similarity_threshold=0.96):
        init_cache_db()
        self.embeddings_model = GeminiEmbeddings()
        self.similarity_threshold = similarity_threshold

    def get_cached_response(self, query_text: str) -> str:
        """
        Calculates the embedding of the query and compares it against all cached queries.
        Returns the cached response if similarity > threshold.
        """
        try:
            # 1. Embed the incoming query
            query_emb = self.embeddings_model.embed_query(query_text)
            
            # 2. Fetch all cached items
            conn = sqlite3.connect(CACHE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT query_text, embedding_json, response_text FROM semantic_cache")
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return None
                
            # 3. Find the most similar cached query
            best_match = None
            highest_sim = -1.0
            
            for row in rows:
                cached_query, emb_json, response = row
                cached_emb = json.loads(emb_json)
                
                sim = cosine_similarity(query_emb, cached_emb)
                if sim > highest_sim:
                    highest_sim = sim
                    best_match = response
                    
            if highest_sim >= self.similarity_threshold:
                logger.info(f"CACHE HIT (Sim: {highest_sim:.3f}): '{query_text}'")
                return best_match
                
            return None
        except Exception as e:
            logger.error(f"Semantic Cache Error (get): {e}")
            return None

    def set_cached_response(self, query_text: str, response_text: str):
        """
        Saves the query, its embedding, and the response to the SQLite cache.
        """
        try:
            query_emb = self.embeddings_model.embed_query(query_text)
            emb_json = json.dumps(query_emb)
            
            conn = sqlite3.connect(CACHE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO semantic_cache (query_text, embedding_json, response_text, created_at)
                VALUES (?, ?, ?, ?)
            ''', (query_text, emb_json, response_text, time.time()))
            conn.commit()
            conn.close()
            logger.info(f"Stored query in semantic cache: '{query_text[:50]}...'")
        except Exception as e:
            logger.error(f"Semantic Cache Error (set): {e}")
