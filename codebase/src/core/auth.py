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
        CREATE TABLE IF NOT EXISTS ADMIN_USER (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    ''')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM ADMIN_USER")
        if cursor.fetchone()[0] == 0:
            import time
            cursor.execute("INSERT INTO ADMIN_USER (id, username, hashed_password, role, created_at) SELECT id, username, password_hash, role, ? FROM users", (time.time(),))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES ADMIN_USER(id)
        )
    ''')
    
    cursor.execute("SELECT id FROM ADMIN_USER WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pw = settings.ADMIN_PASSWORD
        if not admin_pw:
            admin_pw = secrets.token_urlsafe(12)
            logging.getLogger("DATN-Auth").warning(
                "No ADMIN_PASSWORD set. Generated initial admin password: %s "
                "(set ADMIN_PASSWORD in .env and/or change it after first login)", admin_pw
            )
        cursor.execute("INSERT INTO ADMIN_USER (username, hashed_password, role, created_at) VALUES (?, ?, ?, ?)",
                       ('admin', hash_password(admin_pw), 'admin', time.time()))
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, hashed_password FROM ADMIN_USER WHERE username = ?", (username,))
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
    cursor.execute("SELECT ADMIN_USER.id, ADMIN_USER.username, ADMIN_USER.role, sessions.expires_at FROM sessions JOIN ADMIN_USER ON sessions.user_id = ADMIN_USER.id WHERE sessions.token = ?", (token,))
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
    cursor.execute("SELECT id, username, role FROM ADMIN_USER")
    users = [{"id": r[0], "username": r[1], "role": r[2]} for r in cursor.fetchall()]
    conn.close()
    return users

def create_user(username, password, role="admin"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ADMIN_USER (username, hashed_password, role, created_at) VALUES (?, ?, ?, ?)",
                       (username, hash_password(password), role, time.time()))
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
    cursor.execute("DELETE FROM ADMIN_USER WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
def update_user(user_id, username=None, password=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if username and password:
            cursor.execute("UPDATE ADMIN_USER SET username = ?, hashed_password = ? WHERE id = ?", (username, hash_password(password), user_id))
        elif username:
            cursor.execute("UPDATE ADMIN_USER SET username = ? WHERE id = ?", (username, user_id))
        elif password:
            cursor.execute("UPDATE ADMIN_USER SET hashed_password = ? WHERE id = ?", (hash_password(password), user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
