import sqlite3

def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn

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
    conn.commit()
    conn.close()
# Main block to run directly
if __name__ == "__main__":
    create_user_table()
<<<<<<< HEAD
    print("✅ users table created (if it didn't already exist).")
=======
    print("✅ users table created (if it didn't already exist).")
>>>>>>> 56cec695fe366cc576c18539cab85fcd1021dee0
