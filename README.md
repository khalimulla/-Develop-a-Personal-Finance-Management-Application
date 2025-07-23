 # User Authentication System (Python + SQLite)

 This is a simple command-line based user authentication system built with Python and SQLite. It allows users to:

Register a new account with a unique username and password.

Securely hash passwords using SHA-256.

Log in with existing credentials.

 # Tech Stack :
Language: Python 3

Database: SQLite (local file-based)

Security: Passwords are hashed with hashlib (SHA-256)

# Project Structure

├── users.db                # SQLite database (created automatically)
└── auth_app.py             # Main application file


 # Features         
Create a local SQLite database and user table automatically.

Register new users with hashed passwords.

Login with credentials and verify against the database.

Handles duplicate usernames.

Secure password hashing.

# Requirements :
Python 3.13.5

# Installation & Usage
1.Clone the repository or download the script

https://github.com/khalimulla/personal-finance-cli

2.Run the app

3.Follow the menu:

Press 1 to Register

Press 2 to Login

Press 3 to Exit

# Sample Output
 Welcome to Personal Finance Manager

1. Register
2. Login
3. Exit
Enter your choice: 1
Enter username: john123
Enter password: ********
 Registration successful!

# Security Notes

Passwords are hashed using SHA-256 but not salted. For production, consider using libraries like bcrypt or argon2.

No email verification or password recovery implemented in this version



