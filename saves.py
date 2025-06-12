import os
import json

TASKS_DIR = os.path.join(os.path.dirname(__file__), "users", "tasks")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users", "users.json")
ATTEMPTS_FILE = os.path.join(os.path.dirname(__file__), "users", "security.log")

def save_users(users):
    """
    Save the users dictionary to the users JSON file.
    """
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def save_attempts(attempts):
    """
    Save the login attempts dictionary to the security log file in JSON format.
    """
    os.makedirs(os.path.dirname(ATTEMPTS_FILE), exist_ok=True)
    with open(ATTEMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(attempts, f, indent=4)

def save_tasks(username, tasks):
    """
    Save the list of tasks for a specific user.
    """
    os.makedirs(TASKS_DIR, exist_ok=True)
    tasks_file = os.path.join(TASKS_DIR, f"{username}_tasks.json")
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)