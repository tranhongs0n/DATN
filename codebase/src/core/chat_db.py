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

