from loads import load_users, load_attempts
from login import login
from register import register

users = load_users()
attempts = load_attempts()

def print_menu():
    print("=" * 40)
    print("        Welcome to My_tasks_App!")
    print("=" * 40)
    print("Please choose an option:")
    print("  1. Login")
    print("  2. Register")
    print("  3. Create admin")
    print("  0. Exit")
    print("=" * 40)

def main_menu():
    while True:
        print_menu()
        try:
            choice = input("Enter your choice: ").strip()
            if not choice.isdigit():
                raise TypeError("Please enter a number (0, 1, 2, or 3).")
            if choice not in ['0', '1', '2', '3']:
                raise ValueError("Option out of range. Please choose 0, 1, 2, or 3.")
            if choice == '1':
                login(users, attempts)
            elif choice == '2':
                register(users, admin=False)
            elif choice == '3':
                admin_pass = input("Enter admin creation password: ").strip()
                if admin_pass == "cesae123":
                    register(users, admin=True)
                else:
                    print("Incorrect admin password. Access denied.")
                    input("Press Enter to return to the main menu...")
                    continue  # Volta ao menu inicial
            elif choice == '0':
                print("\nThank you for using My_tasks_App. Goodbye!")
                break
        except TypeError as te:
            print(f"\n{te}")
            input("Press Enter to continue...")
        except ValueError as ve:
            print(f"\n{ve}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()