import sqlite3
import hashlib

def get_db_connection():
    return sqlite3.connect("users.db")

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        print(" Registration successful!")
    except sqlite3.IntegrityError:
        print(" Username already exists. Try another.")
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    if user:
        print(f" Login successful! Welcome, {username}!")
        return True
    else:
        print(" Login failed. Incorrect username or password.")
        return False

def main():
    create_user_table()
    print(" Welcome to Personal Finance Manager")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password):
                print(" You are now logged in. More features coming soon...")
                break  # proceed to next feature later

        elif choice == '3':
            print(" Goodbye!")
            break

        else:
            print(" Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

