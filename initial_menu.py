"""
Task Manager Application - Main Menu Module

This module provides the initial menu interface for the Task Manager application.
It handles user authentication, registration, and admin creation functionality.

Features:
- User login with authentication
- New user registration
- Admin account creation (with admin password verification)
- Clean, colored menu interface
- Error handling and user feedback

The module serves as the entry point for the application, directing users
to appropriate functionality based on their menu selection.
"""

import hashlib

from loads import load_users, load_attempts, get_admin_password_hash
from login import login
from register import register
from screen_utils import clear_screen, display_last_action, display_full_screen_menu, centered_input
from password_utils import get_password_with_asterisks
from colors import Colors, success, error, warning, info, prompt

users = load_users()
attempts = load_attempts()

def print_menu():
    """
    Display the main menu interface for the Task Manager application.

    This function presents a full screen formatted menu with the following options:
    - Login: Authenticate existing users
    - Register: Create new user accounts
    - Create admin: Create administrator accounts (requires admin password)
    - Exit: Close the application

    The menu is displayed with full screen presentation and colored text.
    """
    menu_items = [
        f"{Colors.GREEN}  1. {Colors.WHITE}Login",
        f"{Colors.BLUE}  2. {Colors.WHITE}Register",
        f"{Colors.MAGENTA}  3. {Colors.WHITE}Create admin",
        f"{Colors.RED}  0. {Colors.WHITE}Exit"
    ]

    display_full_screen_menu(
        menu_items,
        "Welcome to My_tasks_App!",
        "Task Management System"
    )

def main_menu():
    """
    Main application loop that handles user interaction and menu navigation.

    This function provides the core functionality of the Task Manager application's
    initial interface. It continuously displays the menu, processes user input,
    and directs users to appropriate functionality based on their choices.

    Menu Options:
        1. Login - Authenticate existing users and redirect to task management
        2. Register - Create new user accounts with password validation
        3. Create admin - Create administrator accounts (requires admin password)
        0. Exit - Gracefully terminate the application

    Features:
        - Input validation with appropriate error messages
        - Last action tracking and display for user feedback
        - Exception handling for robust error management
        - Colored output for better user experience
        - Continuous loop until user chooses to exit

    The function maintains state for the last command executed and its result,
    providing visual feedback to users about their previous actions.
    """
    last_command = None
    last_result = None

    while True:
        print_menu()


        if last_command and last_result:
            display_last_action(last_command, last_result)

        try:
            choice = centered_input(prompt("Enter your choice: ")).strip()
            if not choice.isdigit():
                raise TypeError("Please enter a number (0, 1, 2, or 3).")
            if choice not in ['0', '1', '2', '3']:
                raise ValueError("Option out of range. Please choose 0, 1, 2, or 3.")

            if choice == '1':
                last_command = success("Login")
                try:
                    login_result = login(users, attempts)
                    if login_result:
                        last_result = success("Login successful")
                    else:
                        last_result = error("Login failed")
                except (KeyError, FileNotFoundError, ValueError) as e:
                    last_result = error(f"Login error: {str(e)}")
                # No input needed here as login function handles its own pauses

            elif choice == '2':
                last_command = info("Register new user")
                try:
                    register_result = register(users, admin=False)
                    if register_result:
                        last_result = success("Registration successful")
                    else:
                        last_result = error("Registration failed or cancelled")
                except (KeyError, FileNotFoundError, ValueError) as e:
                    last_result = error(f"Registration error: {str(e)}")
                # No input needed here as register function handles its own pauses

            elif choice == '3':
                last_command = f"{Colors.MAGENTA}Create admin{Colors.RESET}"
                admin_pass = get_password_with_asterisks(warning("Enter admin creation password: "))

                # Handle if user cancelled password input
                if admin_pass is None:
                    last_result = warning("Admin creation cancelled")
                    print(f"\n{last_result}")
                    input("Press Enter to continue...")
                else:
                    # Hash the entered password and compare with stored hash
                    entered_password_hash = hashlib.sha256(admin_pass.encode()).hexdigest()
                    stored_admin_hash = get_admin_password_hash()

                    if stored_admin_hash and entered_password_hash == stored_admin_hash:
                        try:
                            admin_register_result = register(users, admin=True)
                            if admin_register_result:
                                last_result = success("Admin creation successful")
                            else:
                                last_result = error("Admin creation failed or cancelled")
                        except (KeyError, FileNotFoundError, ValueError) as e:
                            last_result = error(f"Admin creation error: {str(e)}")
                        # No input needed here as register function handles its own pauses
                    else:
                        last_result = error("Incorrect admin password. Access denied.")
                        print(f"\n{last_result}")
                        input("Press Enter to continue...")

            elif choice == '0':
                clear_screen()
                print(success("\nThank you for using My_tasks_App. Goodbye!"))
                break

        except TypeError as te:
            last_command = error(f"Invalid input: {choice}")
            last_result = error(str(te))
            input("Press Enter to continue...")
        except ValueError as ve:
            last_command = error(f"Invalid option: {choice}")
            last_result = error(str(ve))
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
