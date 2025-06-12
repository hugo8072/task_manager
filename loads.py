"""
Module for loading users and login attempts from JSON files.
"""

import os
import json

TASKS_DIR = os.path.join(os.path.dirname(__file__), "users", "tasks")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users", "users.json")
ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "users", "security.log")

def load_users():
    """
    Load user data from the users JSON file.

    Returns:
        dict: Dictionary with usernames as keys and hashed passwords as values.
    """
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}

def load_attempts():
    """
    Load login attempts data from the security log JSON file.

    Returns:
        dict: Dictionary with usernames as keys and attempt info as values.
    """
    if not os.path.exists(ATTEMPTS_FILE):
        return {}
    try:
        with open(ATTEMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}
    



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
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)