"""
Module for loading users and login attempts from JSON files.
"""

import os
import json

TASKS_DIR = os.path.join(os.path.dirname(__file__), "users", "tasks")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users", "users.json")
ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "users", "security.log")
USERS_ENV_FILE = os.path.join(os.path.dirname(__file__), "users", "users.env")

def _load_env_file(file_path):
    """
    Load environment variables from a .env file.

    Args:
        file_path (str): Path to the .env file

    Returns:
        dict: Dictionary with environment variables
    """
    env_vars = {}
    if not os.path.exists(file_path):
        return env_vars

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    except (OSError, IOError):
        pass

    return env_vars

def load_users_env():
    """
    Load user environment variables from users.env file.

    Returns:
        dict: Dictionary with user environment variables
    """
    return _load_env_file(USERS_ENV_FILE)

def get_admin_password_hash():
    """
    Get the admin password hash from users.env file.

    Returns:
        str: Admin password hash or None if not found
    """
    users_env = load_users_env()
    return users_env.get('ADMIN_PASSWORD')

def _load_json_file(file_path, is_list=False):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file
        is_list (bool): If True, returns empty list as default, otherwise empty dict

    Returns:
        dict or list: JSON data from file, or empty dict/list if file doesn't exist
    """
    default_value = [] if is_list else {}

    if not os.path.exists(file_path):
        return default_value

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return default_value

def load_users():
    """
    Load user data from the users JSON file.

    Returns:
        dict: Dictionary with usernames as keys and hashed passwords as values.
    """
    return _load_json_file(USERS_FILE)  # dict por default

def load_attempts():
    """
    Load login attempts data from the security log JSON file.

    Returns:
        dict: Dictionary with usernames as keys and attempt info as values.
    """
    return _load_json_file(ATTEMPTS_FILE)  # dict por default


def get_user_password_hash(username):
    """
    Get a user's password hash from users.env file.
    Username lookup is case-insensitive.

    Args:
        username (str): The username

    Returns:
        str: Password hash or None if not found
    """
    users_env = load_users_env()

    # Normalize username to lowercase
    username_normalized = username.lower()
    password_key = f"{username_normalized}_password"

    return users_env.get(password_key)

def load_tasks(username):
    """
    Get the path to the tasks file for a specific user and load the list of tasks.
    If the file does not exist, returns an empty list.

    Args:
        username (str): The username whose tasks to load.

    Returns:
        list: List of tasks for the user.
    """
    tasks_dir = os.path.join(os.path.dirname(__file__), "users", "tasks")
    os.makedirs(tasks_dir, exist_ok=True)
    tasks_file = os.path.join(tasks_dir, f"{username}_tasks.json")

    return _load_json_file(tasks_file, is_list=True)  # tasks são armazenadas em lista
