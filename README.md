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

users.db                # SQLite database (created automatically)
 auth_app.py             # Main application file


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
# Once logged in, users can
1. Add Transaction
2. View Transactions
3. Update Transaction
4. Delete Transaction
5. Financial Report
6. Set Budget
7. Backup Data
8. Restore Data
9. Logout
#  Feature Descriptions
  Option | Feature                 Description                                              
 ------  ----------------------  -------------------------------------------------------- 
 1       **Add Transaction**     Add an income or expense with date, category, and amount 
 2       **Update Transaction**  Modify an existing transaction’s details                 
 4       **View Transactions**   See all transactions by date, category, and amount       
 5       **Set Budget**          Define a monthly budget for each category                
 6       **Generate Report**     Summarize income, expenses, and savings by month/year    
 7       **Backup DB**           Create a backup of the current database                  
 8       **Restore DB**          Restore from the previously saved backup                 
 9       **Logout**              Exit the logged-in session                               









