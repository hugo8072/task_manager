import hashlib
from datetime import datetime, timedelta
from saves import save_attempts
from task_manager import task_menu
from task_manager_admin import admin_menu

MAX_ATTEMPTS = 5
BLOCK_MINUTES = 30

def login(users, attempts):
    """
    Handle the login process, including password checking and blocking after 5 failed attempts.
    This function checks if the username exists, verifies the password, and manages login attempts.
    If the user exceeds the maximum number of attempts, they are blocked for a specified duration.
    It saves the updated attempts dictionary to the security log file.

    Args:
        users (dict): Dictionary with usernames as keys and hashed passwords as values.
        attempts (dict): Dictionary with usernames as keys and attempt info as values.
    """
    print("=" * 40)
    print("             Login Page")
    print("=" * 40)
    username = input("Username: ").strip()

    if username not in users:
        print("\nUsername does not exist.")
        input("Press Enter to return to the main menu...")
        return

    now = datetime.now()
    user_attempt = attempts.get(username, {"attempts": 0, "blocked_until": None})

    # Check if user is blocked
    if user_attempt["blocked_until"]:
        blocked_until = datetime.fromisoformat(user_attempt["blocked_until"])
        if now < blocked_until:
            print(f"\nToo many failed attempts. Try again at {blocked_until.strftime('%Y-%m-%d %H:%M:%S')}\n")
            input("Press Enter to return to the main menu...")
            return
        else:
            user_attempt = {"attempts": 0, "blocked_until": None}

    while True:
        password = input("Password: ").strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if users[username]["password"] == hashed_password:
            print(f"\nWelcome, {username}!\n")
            user_attempt = {"attempts": 0, "blocked_until": None}
            attempts[username] = user_attempt
            save_attempts(attempts)
            if users[username].get("admin", False):
                admin_menu()
            else:
                task_menu(username)
            return
        else:
            user_attempt["attempts"] = user_attempt.get("attempts", 0) + 1
            if user_attempt["attempts"] >= MAX_ATTEMPTS:
                blocked_until = now + timedelta(minutes=BLOCK_MINUTES)
                user_attempt["blocked_until"] = blocked_until.isoformat()
                print(f"\nToo many failed attempts. Login blocked until {blocked_until.strftime('%Y-%m-%d %H:%M:%S')}\n")
                break
            else:
                print("\nInvalid password.")
                print(f"Attempt {user_attempt['attempts']} of {MAX_ATTEMPTS}.")
                opt = input("Try again? (y/n): ").strip().lower()
                if opt != 'y':
                    break

    attempts[username] = user_attempt
    save_attempts(attempts)
    input("Press Enter to return to the main menu...")
