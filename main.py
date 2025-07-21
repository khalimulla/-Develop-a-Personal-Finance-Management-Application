from db import create_user_table

def main():
    create_user_table()
    print("Welcome to Personal Finance Manager")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username,password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password):
                break  # proceed to next feature later
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
