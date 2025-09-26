import sqlite3
import hashlib

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            plan TEXT DEFAULT 'Free'
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email: str, name: str, password: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
                  (email.lower(), name, hash_password(password)))
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Email already registered"

def authenticate_user(email: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, email, name, password, plan FROM users WHERE email=?", (email.lower(),))
    user = c.fetchone()
    conn.close()
    if user and user[3] == hash_password(password):
        return True, {"id": user[0], "email": user[1], "name": user[2], "plan": user[4]}
    return False, None

def get_user_by_email(email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, email, name, plan FROM users WHERE email=?", (email.lower(),))
    user = c.fetchone()
    conn.close()
    return user
