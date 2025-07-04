"""
Task Manager Application - User Authentication Module

This module handles user authentication and login functionality for the Task Manager.
It provides secure login mechanisms with attempt tracking, account blocking,
and role-based redirection.

Features:
- Secure password verification using PBKDF2 with SHA256 and salt
- Login attempt tracking and failed attempt limits
- Temporary account blocking after too many failed attempts
- Role-based redirection (admin vs regular user)
- Password input masking for security
- Time-based blocking with automatic unblocking

Security Features:
- Maximum login attempts limit (5 attempts)
- Account blocking for 30 minutes after failed attempts
- Secure password hashing comparison with salt support
- Input validation and sanitization

The module ensures secure access to the Task Manager while providing
appropriate feedback and protection against brute force attacks.
"""

import hashlib
from datetime import datetime, timedelta

from saves import save_attempts
from loads import get_user_password_hash
from task_manager_user import task_menu
from task_manager_admin import admin_main_menu
from screen_utils import clear_screen, display_full_screen_header
from password_utils import get_password_with_asterisks
from colors import success, error, warning, prompt

MAX_ATTEMPTS = 5
BLOCK_MINUTES = 30

def verify_password(password, stored_hash):
    """
    Verify a password against a stored hash with salt.

    Args:
        password (str): The plain text password to verify
        stored_hash (str): The stored hash in format "salt:hash"

    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        # Check if it's old format (no salt) or new format (with salt)
        if ':' not in stored_hash:
            # Old format - SHA256 without salt (backward compatibility)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return stored_hash == hashed_password
        else:
            # New format - PBKDF2 with salt
            salt, hash_hex = stored_hash.split(':', 1)
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hash_hex == password_hash.hex()
    except (ValueError, TypeError):
        return False

def login(users, attempts):
    """
    Handle the login process, including password checking and blocking after 5 failed attempts.
    This function checks if the username exists, verifies the password, and manages login attempts.
    If the user exceeds the maximum number of attempts, they are blocked for a specified duration.
    It saves the updated attempts dictionary to the security log file.

    Args:
        users (dict): Dictionary with usernames as keys and hashed passwords as values.
        attempts (dict): Dictionary with usernames as keys and attempt info as values.

    Returns:
        bool: True if login successful, False if login failed
    """
    clear_screen()
    display_full_screen_header("Login Page", "Enter your credentials")
    username = input(prompt("Username: ")).strip()

    # Find user case-insensitively
    user_found = None
    for user_key in users.keys():
        if user_key.lower() == username.lower():
            user_found = user_key
            break

    if user_found is None:
        print(error("\nUsername does not exist."))
        input("Press Enter to return to the main menu...")
        return False

    # Use the actual username from the database
    username = user_found

    now = datetime.now()
    user_attempt = attempts.get(username, {"attempts": 0, "blocked_until": None})

    # Check if user is blocked
    if user_attempt["blocked_until"]:
        blocked_until = datetime.fromisoformat(user_attempt["blocked_until"])
        if now < blocked_until:
            blocked_time = blocked_until.strftime('%Y-%m-%d %H:%M:%S')
            print(error(f"\nToo many failed attempts. Try again at {blocked_time}\n"))
            input("Press Enter to return to the main menu...")
            return False
        else:
            user_attempt = {"attempts": 0, "blocked_until": None}

    while True:
        password = get_password_with_asterisks(prompt("Password: "))

        # Handle if user cancelled password input
        if password is None:
            print(warning("Login cancelled."))
            input("Press Enter to return to the main menu...")
            return False

        password = password.strip()

        # Get user's password hash from users.env
        stored_password_hash = get_user_password_hash(username)

        if stored_password_hash and verify_password(password, stored_password_hash):
            print(success(f"\nWelcome, {username}!\n"))
            user_attempt = {"attempts": 0, "blocked_until": None}
            attempts[username] = user_attempt
            save_attempts(attempts)
            clear_screen()
            if users[username].get("admin", False):
                admin_main_menu()
            else:
                task_menu(username)
            return True
        else:
            user_attempt["attempts"] = user_attempt.get("attempts", 0) + 1
            if user_attempt["attempts"] >= MAX_ATTEMPTS:
                blocked_until = now + timedelta(minutes=BLOCK_MINUTES)
                user_attempt["blocked_until"] = blocked_until.isoformat()
                print(error(f"\nToo many failed attempts. Login blocked until "
                            f"{blocked_until.strftime('%Y-%m-%d %H:%M:%S')}\n"))
                break
            else:
                print(error("\nInvalid password."))
                print(warning(f"Attempt {user_attempt['attempts']} of {MAX_ATTEMPTS}."))
                opt = input(prompt("Try again? (y/n): ")).strip().lower()
                if opt != 'y':
                    break

    attempts[username] = user_attempt
    save_attempts(attempts)
    input("Press Enter to return to the main menu...")
    return False
