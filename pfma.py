import sqlite3
import hashlib
import shutil
import os
from datetime import datetime

DB_FILE = "users.db"
BACKUP_FILE = "backup_users.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE)

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
            date TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL
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
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
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
        return True
    else:
        return False

def add_transaction(username):
    amount = float(input("Amount: "))
    type_ = input("Type (income/expense): ").lower()
    category = input("Category: ")
    date = input("Date (YYYY-MM-DD): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (username, amount, type, category, date)
        VALUES (?, ?, ?, ?, ?)
    """, (username, amount, type_, category, date))
    conn.commit()
    conn.close()
    print("Transaction added.")

def update_transaction(username):
    id_ = int(input("Transaction ID to update: "))
    amount = float(input("New amount: "))
    category = input("New category: ")
    date = input("New date (YYYY-MM-DD): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions
        SET amount=?, category=?, date=?
        WHERE id=? AND username=?
    """, (amount, category, date, id_, username))
    conn.commit()
    conn.close()
    print("Transaction updated.")

def delete_transaction(username):
    id_ = int(input("Transaction ID to delete: "))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=? AND username=?", (id_, username))
    conn.commit()
    conn.close()
    print("Transaction deleted.")

def view_transactions(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, type, category, date FROM transactions WHERE username=?", (username,))
    rows = cursor.fetchall()
    conn.close()

    print("\nYour Transactions:")
    for row in rows:
        print(f"ID: {row[0]} | ₹{row[1]} | {row[2]} | {row[3]} | {row[4]}")

def set_budget(username):
    category = input("Category: ")
    amount = float(input("Monthly Budget Amount: "))
    month = input("Month (YYYY-MM): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (username, category, amount, month)
        VALUES (?, ?, ?, ?)
    """, (username, category, amount, month))
    conn.commit()
    conn.close()
    print("Budget set.")

def generate_financial_report(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    year = input("Enter year (YYYY): ").strip()
    month_input = input("Enter month (1-12) or leave blank for yearly report: ").strip()

    try:
        if month_input:
            month = int(month_input)
            cursor.execute("""
                SELECT type, SUM(amount)
                FROM transactions
                WHERE username = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
                GROUP BY type
            """, (username, year, f"{month:02d}"))
        else:
            cursor.execute("""
                SELECT type, SUM(amount)
                FROM transactions
                WHERE username = ? AND strftime('%Y', date) = ?
                GROUP BY type
            """, (username, year))

        rows = cursor.fetchall()
        income = expense = 0.0
        for row in rows:
            if row[0] == 'income':
                income = row[1] or 0.0
            elif row[0] == 'expense':
                expense = row[1] or 0.0

        savings = income - expense
        print(f"Total Income: ₹{income:.2f}")
        print(f"Total Expenses: ₹{expense:.2f}")
        print(f"Savings: ₹{savings:.2f}")

    except Exception as e:
        print("Error generating report:", e)

    finally:
        conn.close()

def backup_database():
    if os.path.exists(DB_FILE):
        shutil.copy(DB_FILE, BACKUP_FILE)
        print("Database backup created.")
    else:
        print("Database not found.")

def restore_database():
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, DB_FILE)
        print("Database restored from backup.")
    else:
        print("Backup not found.")

def main():
    create_user_table()
    print("Welcome to Personal Finance Manager")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            register_user(username, password)

        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            if login_user(username, password):
                while True:
                    print("\n1. Add Transaction\n2. Update Transaction\n3. Delete Transaction")
                    print("4. View Transactions\n5. Set Budget\n6. Generate Report")
                    print("7. Backup DB\n8. Restore DB\n9. Logout")
                    inner_choice = input("Enter choice: ")

                    if inner_choice == '1':
                        add_transaction(username)
                    elif inner_choice == '2':
                        update_transaction(username)
                    elif inner_choice == '3':
                        delete_transaction(username)
                    elif inner_choice == '4':
                        view_transactions(username)
                    elif inner_choice == '5':
                        set_budget(username)
                    elif inner_choice == '6':
                        generate_financial_report(username)
                    elif inner_choice == '7':
                        backup_database()
                    elif inner_choice == '8':
                        restore_database()
                    elif inner_choice == '9':
                        break
                    else:
                        print("Invalid choice.")
            else:
                print("Login failed.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()   




