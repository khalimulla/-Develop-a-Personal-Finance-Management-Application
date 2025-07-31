&nbsp; Personal Finance Management Application – User Manual



&nbsp; Table of Contents

1\. \[Introduction](#introduction)  

2\. \[Features](#features)  

3\. \[Installation](#installation)  

4\. \[Usage Guide](#usage-guide)  

&nbsp;   - \[Register \& Login](#register--login)  

&nbsp;   - \[Add Transaction](#add-transaction)  

&nbsp;   - \[Update Transaction](#update-transaction)  

&nbsp;   - \[Delete Transaction](#delete-transaction)  

&nbsp;   - \[View Transactions](#view-transactions)  

&nbsp;   - \[Generate Reports](#generate-reports)  

&nbsp;   - \[Set Budget](#set-budget)  

&nbsp;   - \[Backup \& Restore Data](#backup--restore-data)  

5\. \[Testing](#testing)  

6\. \[Best Practices](#best-practices)  

7\. \[Troubleshooting](#troubleshooting)  



1\.  Introduction

The \*\*Personal Finance Management App\*\* is a command-line tool to help users manage income, expenses, budgeting, and reports—all saved securely in a local SQLite database. It supports user authentication and data backup.



&nbsp; Features

\- User Registration \& Login with SHA-256 password hashing  

\- Income \& Expense Tracking (with categories like Food, Salary, Rent, etc.)  

\- Monthly \& Yearly Financial Reports  

\- Budget Tracking \& Alerts  

\- SQLite3-based local storage  

\- Data Backup \& Restore  

\- Unit Testing for all core features  



&nbsp; Installation

1\. Clone or download the project folder:

&nbsp;  ```bash

&nbsp;  git clone https://github.com/yourusername/personal-finance-manager.git

&nbsp;  cd personal-finance-manager

&nbsp;  ```



2\. Install required Python packages:

&nbsp;  ```bash

&nbsp;  pip install tabulate

&nbsp;  ```



3\. Run the application:

&nbsp;  ```bash

&nbsp;  python app.py

&nbsp;  ```



&nbsp; Usage Guide



&nbsp; Register \& Login

\- On startup, choose:  

&nbsp; - `1. Register`: Create a new account  

&nbsp; - `2. Login`: Access your dashboard  

\- Passwords are securely hashed.



&nbsp;Add Transaction

After login, choose:  

`1. Add Transaction`  

Enter:  

\- Date (YYYY-MM-DD)  

\- Type (`income` or `expense`)  

\- Category (e.g., Salary, Food)  

\- Amount  

\- Description (optional)  



&nbsp; Update Transaction

Choose: `2. Update Transaction`  

\- Provide transaction ID to update.  

\- Change any detail (amount, category, etc.).



&nbsp; Delete Transaction

Choose: `3. Delete Transaction`  

\- Enter transaction ID to remove it from your list.



&nbsp; View Transactions

Choose: `4. View Transactions`  

\- View all your records in a tabular format.  

\- Filter by date or category if needed.



&nbsp; Generate Reports

Choose: `5. Generate Report`  

\- Choose monthly or yearly.  

Example Output:  

```

March 2025:

Income: Rs. 45,000

Expenses: Rs. 32,000

Savings: Rs. 13,000

```



&nbsp; Set Budget

Choose: `6. Set/View Budget`  

\- Set monthly category-wise budget (e.g., Rs. 10,000 for Food).  

\- App notifies if you exceed it during the month.



&nbsp; Backup \& Restore Data

Choose: `7. Backup Data` or `8. Restore Data`  

\- \*\*Backup\*\*: Saves a copy of `users.db` to `backup\_users.db`  

\- \*\*Restore\*\*: Restores from backup if needed



&nbsp; Testing

&nbsp;Unit Tests

All core features (authentication, transactions, reporting) are covered using `unittest`.



To run tests:  

```bash

python -m unittest discover tests/

```



Example test structure:

```

tests/

├── test\_auth.py

├── test\_transactions.py

├── test\_reports.py

└── test\_budget.py

```



\##  Best Practices

\- Use strong passwords  

\- Regularly backup your data  

\- Use meaningful categories and descriptions  

\- Check your reports weekly or monthly



\## Troubleshooting



| Problem                        | Solution                                             |

|-------------------------------|------------------------------------------------------|

| App crashes on start          | Ensure Python 3 is installed properly.               |

| Login not working             | Check if you're registered with the correct username |

| Can't find the database file  | Make sure `users.db` is in the project folder.       |

| Errors during backup/restore  | Check read/write permissions in the folder.          |



