"""
Task Manager Application - User Registration Module

This module handles user registration and account creation functionality.
It provides secure user registration with input validation, password verification,
and role-based account creation (regular users and administrators).

Features:
- Secure user registration with username validation
- Password strength validation and confirmation
- Admin account creation with special privileges
- Input sanitization and error handling
- Duplicate username prevention
- Password hashing using PBKDF2 with SHA256 and unique salt per user
- User-friendly interface with colored output

Security Features:
- Password masking during input
- Strong password requirements validation
- Secure password storage using PBKDF2 with SHA256 and unique salt
- Username uniqueness validation
- Input validation and sanitization

The module ensures secure account creation while providing clear feedback
to users throughout the registration process.
"""

import hashlib
import secrets

from saves import save_users, save_user_password
from screen_utils import clear_screen, display_full_screen_header
from password_utils import get_password_with_asterisks
from colors import success, error, warning, prompt

def register(users, admin=False):
    """
    Handle the user registration process, including username and password validation.
    Allows creation of admin users if admin=True.

    Args:
        users (dict): Dictionary with usernames as keys and user info as values.
        admin (bool): If True, creates an admin user. Defaults to False.

    Returns:
        bool: True if registration successful, False if registration failed or cancelled
    """
    clear_screen()
    display_full_screen_header(
        "Register Page" + (" (Admin)" if admin else ""),
        "Create your account"
    )
    while True:
        username = input(prompt("Choose a username: ")).strip()

        # Normalize username to lowercase for comparison
        username_lower = username.lower()

        # Check if username already exists (case-insensitive)
        existing_users_lower = {k.lower(): k for k in users.keys()}

        if username_lower in existing_users_lower:
            print(error(f"Username '{username_lower}' already exists. Please choose another name."))
        elif not username:
            print(error("Username cannot be empty."))
        else:
            # Use the original case provided by user
            break

    password = get_password_with_asterisks(prompt("Choose a password: "))

    # Handle if user cancelled password input
    if password is None:
        print(warning("Registration cancelled. Password must be provided."))
        input("Press Enter to return to the main menu...")
        return False

    password = password.strip()

    # Save user metadata (without password)
    users[username] = {
        "admin": admin
    }
    save_users(users)

    # Save password hash separately with salt
    # Generate a unique salt for this user
    salt = secrets.token_hex(16)  # 32 character hex string
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    password_hash_hex = password_hash.hex()

    # Save both salt and hash
    save_user_password(username, f"{salt}:{password_hash_hex}")

    print(success(f"\nUser '{username}' registered successfully!"
    + (" (Admin)" if admin else "") + "\n"))
    input("Press Enter to return to the main menu...")
    return True
