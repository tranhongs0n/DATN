import sqlite3
import bcrypt
import secrets
import os
import time
import logging
from src.config.settings import settings

DB_PATH = settings.DATA_DIR / "auth.db"

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def init_db():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pw = settings.ADMIN_PASSWORD
        if not admin_pw:
            admin_pw = secrets.token_urlsafe(12)
            logging.getLogger("DATN-Auth").warning(
                "No ADMIN_PASSWORD set. Generated initial admin password: %s "
                "(set ADMIN_PASSWORD in .env and/or change it after first login)", admin_pw
            )
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       ('admin', hash_password(admin_pw), 'admin'))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
        return row[0]
    return None

def create_session(user_id):
    token = secrets.token_hex(32)
    expires_at = time.time() + 24 * 3600
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)", (token, user_id, expires_at))
    conn.commit()
    conn.close()
    return token

def get_user_from_token(token):
    if not token: return None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT users.id, users.username, users.role, sessions.expires_at FROM sessions JOIN users ON sessions.user_id = users.id WHERE sessions.token = ?", (token,))
    row = cursor.fetchone()
    conn.close()
    if row:
        if time.time() > row[3]:
            logout_session(token)
            return None
        return {"id": row[0], "username": row[1], "role": row[2]}
    return None

def logout_session(token):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = [{"id": r[0], "username": r[1], "role": r[2]} for r in cursor.fetchall()]
    conn.close()
    return users

def create_user(username, password, role="admin"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, hash_password(password), role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
    return success

def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
def update_user(user_id, username=None, password=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if username and password:
            cursor.execute("UPDATE users SET username = ?, password_hash = ? WHERE id = ?", (username, hash_password(password), user_id))
        elif username:
            cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        elif password:
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password(password), user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
