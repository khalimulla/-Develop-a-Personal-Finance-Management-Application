import sqlite3
import hashlib
import getpass
import shutil
from datetime import datetime

# ---------- Database Connection ----------
def get_db_connection():
    return sqlite3.connect("users.db")

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
    conn.commit()
    conn.close()

def create_transaction_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT DEFAULT (DATE('now'))
        )
    """)
    conn.commit()
    conn.close()

def create_budget_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(username, category, month)
        )
    """)
    conn.commit()
    conn.close()

# ---------- Password Hashing ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- User Registration ----------
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print(" Username already exists. Try another.")
    finally:
        conn.close()

# ---------- User Login ----------
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

# ---------- Input Wrapper ----------
def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, OSError):
        return ""

# ---------- Transaction Features ----------
def add_transaction(username):
    print("\n--- Add Transaction ---")
    type = safe_input("Enter type (income/expense): ").lower()
    if type not in ['income', 'expense']:
        print(" Invalid type.")
        return
    category = safe_input("Enter category (e.g., Food, Rent, Salary): ")
    try:
        amount = float(safe_input("Enter amount: "))
    except ValueError:
        print(" Invalid amount.")
        return
    description = safe_input("Enter description (optional): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (username, type, category, amount, description)
        VALUES (?, ?, ?, ?, ?)
    """, (username, type, category, amount, description))
    conn.commit()

    # Check Budget
    cursor.execute("""
        SELECT amount FROM budgets
        WHERE username = ? AND category = ? AND month = strftime('%Y-%m', 'now')
    """, (username, category))
    budget = cursor.fetchone()
    if budget:
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE username = ? AND category = ? AND type='expense'
            AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """, (username, category))
        spent = cursor.fetchone()[0] or 0
        if spent > budget[0]:
            print("⚠️ Warning: You have exceeded your budget for this category!")

    conn.close()
    print(" Transaction added successfully.")

def view_transactions(username):
    print("\n--- Your Transactions ---")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, category, amount, description, date
        FROM transactions
        WHERE username = ?
        ORDER BY date DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"{row[0]}. [{row[1]}] {row[2]} - ₹{row[3]} | {row[4]} | {row[5]}")
    else:
        print("ℹ️ No transactions found.")

def update_transaction(username):
    view_transactions(username)
    txn_id = safe_input("Enter Transaction ID to update: ")
    try:
        new_amount = float(safe_input("New amount: "))
    except ValueError:
        print(" Invalid amount.")
        return
    new_category = safe_input("New category: ")
    new_description = safe_input("New description: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount=?, category=?, description=?
        WHERE id=? AND username=?
    """, (new_amount, new_category, new_description, txn_id, username))
    conn.commit()
    conn.close()
    print(" Transaction updated.")

def delete_transaction(username):
    view_transactions(username)
    txn_id = safe_input("Enter Transaction ID to delete: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM transactions
        WHERE id=? AND username=?
    """, (txn_id, username))
    conn.commit()
    conn.close()
    print(" Transaction deleted.")

# ---------- Financial Summary ----------
def financial_summary(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            strftime('%Y-%m', date) as month,
            SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as total_income,
            SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as total_expense,
            SUM(CASE WHEN type='income' THEN amount ELSE 0 END) -
            SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as savings
        FROM transactions
        WHERE username = ?
        GROUP BY month
        ORDER BY month DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()

    print("\n Monthly Financial Summary:")
    for row in rows:
        print(f"{row[0]} → Income: ₹{row[1]} | Expense: ₹{row[2]} | Savings: ₹{row[3]}")

# ---------- Budgeting ----------
def set_budget(username):
    category = safe_input("Category: ")
    try:
        amount = float(safe_input("Budget amount: "))
    except ValueError:
        print(" Invalid amount.")
        return
    month = safe_input("Month (YYYY-MM): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO budgets (username, category, amount, month)
        VALUES (?, ?, ?, ?)
    """, (username, category, amount, month))
    conn.commit()
    conn.close()
    print(" Budget set.")

# ---------- Backup & Restore ----------
def backup_data():
    shutil.copy("users.db", "backup_users.db")
    print(" Backup created as 'backup_users.db'")

def restore_data():
    try:
        shutil.copy("backup_users.db", "users.db")
        print(" Data restored from 'backup_users.db'")
    except FileNotFoundError:
        print(" Backup file not found.")

# ---------- Logged-In Menu ----------
def show_logged_in_menu(username):
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Financial Report")
        print("6. Set Budget")
        print("7. Backup Data")
        print("8. Restore Data")
        print("9. Logout")
        choice = safe_input("Enter your choice: ")

        if choice == '1':
            add_transaction(username)
        elif choice == '2':
            view_transactions(username)
        elif choice == '3':
            update_transaction(username)
        elif choice == '4':
            delete_transaction(username)
        elif choice == '5':
            financial_summary(username)
        elif choice == '6':
            set_budget(username)
        elif choice == '7':
            backup_data()
        elif choice == '8':
            restore_data()
        elif choice == '9':
            print("👋 Logged out.")
            break
        else:
            print(" Invalid choice.")

# ---------- Main App ----------
def main():
    create_user_table()
    create_transaction_table()
    create_budget_table()
    print(" Welcome to Personal Finance Manager")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = safe_input("Enter your choice: ").strip()

        if choice == '1':
            username = safe_input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            register_user(username, password)

        elif choice == '2':
            username = safe_input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            if login_user(username, password):
                show_logged_in_menu(username)

        elif choice == '3':
            print(" Goodbye!")
            break

        else:
            print(" Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
