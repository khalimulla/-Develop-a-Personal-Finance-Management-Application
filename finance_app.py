import sqlite3
import hashlib
import os
import shutil

DB_FILE = "users.db"
BACKUP_FILE = "backup_users.db"

# ---------- Utility ----------
def get_db_connection():
    return sqlite3.connect(DB_FILE)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, OSError):
        return ""

# ---------- Table Creation ----------
def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT DEFAULT (date('now'))
    )
""")

