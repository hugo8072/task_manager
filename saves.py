"""
Task Manager Application - Data Persistence Module

This module handles all data saving operations for the Task Manager application.
It provides centralized functionality for persisting user data, tasks, login attempts,
and configuration settings to various file formats.

Features:
- JSON file operations for structured data (users, tasks, login attempts)
- Environment file operations for configuration and passwords
- Automatic directory creation for data organization
- Consistent file formatting with proper indentation
- Error handling for file I/O operations
- Centralized data persistence logic

Data Types Handled:
- User account information (users.json)
- Task data per user (*_tasks.json)
- Login attempt tracking (security.log)
- Password hashes and configuration (users.env)

File Structure:
- users/users.json - User account metadata
- users/tasks/*.json - Individual user task files
- users/security.log - Login attempt tracking
- users/users.env - Password hashes and configuration

The module ensures data integrity and provides a clean interface for all
persistence operations throughout the application.
"""

import os
import json

from loads import load_users_env

TASKS_DIR = os.path.join(os.path.dirname(__file__), "users", "tasks")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users", "users.json")
ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "users", "security.log")
USERS_ENV_FILE = os.path.join(os.path.dirname(__file__), "users", "users.env")

def _save_json_file(file_path, data):
    """
    Save data to a JSON file.

    Args:
        file_path (str): Path to the JSON file
        data: Data to save (dict, list, etc.)
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_users(users):
    """
    Save the users dictionary to the users JSON file.
    """
    _save_json_file(USERS_FILE, users)

def save_attempts(attempts):
    """
    Save the login attempts dictionary to the security log file in JSON format.
    """
    _save_json_file(ATTEMPTS_FILE, attempts)

def save_tasks(username, tasks):
    """
    Save the list of tasks for a specific user.
    """
    tasks_file = os.path.join(TASKS_DIR, f"{username}_tasks.json")
    _save_json_file(tasks_file, tasks)

def save_user_password(username, password_hash):
    """
    Save or update a user's password hash in the users.env file.
    Username is normalized to lowercase for consistency.

    Args:
        username (str): The username
        password_hash (str): The SHA256 hash of the password
    """
    os.makedirs(os.path.dirname(USERS_ENV_FILE), exist_ok=True)

    # Normalize username to lowercase
    username_normalized = username.lower()

    # Read existing content using the common function
    env_content = load_users_env()

    # Update or add the user's password (using normalized username)
    password_key = f"{username_normalized}_password"
    env_content[password_key] = password_hash

    # Write back to file
    with open(USERS_ENV_FILE, "w", encoding="utf-8") as f:
        f.write("# User passwords (SHA256 hashes)\n")
        f.write("# Format: username_password=hash_value\n\n")

        # Write admin password first if it exists
        if "ADMIN_PASSWORD" in env_content:
            f.write("# Admin password for creating admin users\n")
            f.write(f"ADMIN_PASSWORD={env_content['ADMIN_PASSWORD']}\n\n")

        # Write user passwords
        f.write("# User passwords\n")
        for key, value in env_content.items():
            if key != "ADMIN_PASSWORD":
                f.write(f"{key}={value}\n")
