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
    # Auto-migrate if columns missing
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN needs_human INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column already exists
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN rating INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column already exists
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_users (
            user_id TEXT PRIMARY KEY,
            blocked_at REAL NOT NULL,
            reason TEXT
        )
    ''')
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

def get_conversations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Get distinct user_ids with their latest message time, and check if they need human
    cursor.execute('''
        SELECT user_id, MAX(timestamp) as last_msg_time, MAX(needs_human) as needs_human
        FROM messages 
        GROUP BY user_id 
        ORDER BY last_msg_time DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [{"user_id": r[0], "last_activity": r[1], "needs_human": bool(r[2])} for r in rows]

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

def clear_human_flag(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE messages SET needs_human = 0 WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def rate_message(message_id: int, rating: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE messages SET rating = ? WHERE id = ?
    ''', (rating, message_id))
    conn.commit()
    conn.close()

def block_user(user_id: str, reason: str = ""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO blocked_users (user_id, blocked_at, reason) 
        VALUES (?, ?, ?)
    ''', (user_id, time.time(), reason))
    conn.commit()
    conn.close()

def unblock_user(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM blocked_users WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def is_user_blocked(user_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM blocked_users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row)

def get_blocked_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, blocked_at, reason FROM blocked_users ORDER BY blocked_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"user_id": r[0], "blocked_at": r[1], "reason": r[2]} for r in rows]

init_db()
