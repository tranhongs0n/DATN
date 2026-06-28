import sqlite3
import os
import time
from src.config.settings import settings

DB_PATH = settings.DATA_DIR / "chat_history.db"

def init_db():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp REAL NOT NULL,
            needs_human INTEGER DEFAULT 0,
            rating INTEGER DEFAULT 0
        )
    ''')
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN needs_human INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN rating INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
        
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CHAT_SESSION (
            session_id TEXT PRIMARY KEY,
            zalo_user_id TEXT NOT NULL,
            start_time REAL NOT NULL,
            last_interaction REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CHAT_LOG (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            retrieved_context_ids TEXT,
            latency_ms REAL,
            timestamp REAL NOT NULL,
            FOREIGN KEY(session_id) REFERENCES CHAT_SESSION(session_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DOCUMENT_METADATA (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            format TEXT NOT NULL,
            chunk_count INTEGER DEFAULT 0,
            status TEXT NOT NULL,
            uploaded_at REAL NOT NULL,
            uploaded_by INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS abbreviations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_form TEXT UNIQUE NOT NULL,
            full_form TEXT NOT NULL
        )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages (user_id)")
    conn.commit()
    conn.close()

def log_message(user_id: str, role: str, content: str, needs_human: bool = False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id, role, content, timestamp, needs_human)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, role, content, time.time(), 1 if needs_human else 0))
    conn.commit()
    conn.close()

def get_chat_history(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, role, content, timestamp, needs_human, rating
        FROM messages 
        WHERE user_id = ? 
        ORDER BY timestamp ASC
    ''', (user_id,))
    rows = cursor.fetchall()
    
    conn.close()
    return [{"id": r[0], "role": r[1], "content": r[2], "timestamp": r[3], "needs_human": bool(r[4]), "rating": r[5]} for r in rows]

def rate_message(message_id: int, rating: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE messages SET rating = ? WHERE id = ?
    ''', (rating, message_id))
    conn.commit()
    conn.close()

def get_all_abbreviations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, short_form, full_form FROM abbreviations")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "short_form": r[1], "full_form": r[2]} for r in rows]

def add_abbreviation(short_form: str, full_form: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO abbreviations (short_form, full_form) VALUES (?, ?)", (short_form.lower(), full_form))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def update_abbreviation(abbr_id: int, short_form: str, full_form: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE abbreviations SET short_form = ?, full_form = ? WHERE id = ?", (short_form.lower(), full_form, abbr_id))
    conn.commit()
    conn.close()

def delete_abbreviation(abbr_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM abbreviations WHERE id = ?", (abbr_id,))
    conn.commit()
    conn.close()


def log_chat_interaction(user_id: str, user_query: str, bot_response: str, latency_ms: float = 0.0, context_ids: str = ""):
    import uuid
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = time.time()
    
    cursor.execute("SELECT session_id FROM CHAT_SESSION WHERE zalo_user_id = ? AND last_interaction > ? ORDER BY last_interaction DESC LIMIT 1", (user_id, now - 86400))
    row = cursor.fetchone()
    if row:
        session_id = row[0]
        cursor.execute("UPDATE CHAT_SESSION SET last_interaction = ? WHERE session_id = ?", (now, session_id))
    else:
        session_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO CHAT_SESSION (session_id, zalo_user_id, start_time, last_interaction) VALUES (?, ?, ?, ?)", (session_id, user_id, now, now))
        
    cursor.execute('''
        INSERT INTO CHAT_LOG (session_id, user_query, bot_response, retrieved_context_ids, latency_ms, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, user_query, bot_response, context_ids, latency_ms, now))
    
    cursor.execute('''
        INSERT INTO messages (user_id, role, content, timestamp, needs_human)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, 'user', user_query, now - 0.01, 0))
    cursor.execute('''
        INSERT INTO messages (user_id, role, content, timestamp, needs_human)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, 'assistant', bot_response, now, 0))
    
    conn.commit()
    conn.close()
