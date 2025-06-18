import hashlib
from saves import save_users

def register(users, admin=False):
    """
    Handle the user registration process, including username and password validation.
    Allows creation of admin users if admin=True.

    Args:
        users (dict): Dictionary with usernames as keys and user info as values.
        admin (bool): If True, creates an admin user. Defaults to False.
    """
    print("=" * 40)
    print("           Register Page" + (" (Admin)" if admin else ""))
    print("=" * 40)
    while True:
        username = input("Choose a username: ").strip()
        if username in users:
            print("Username already exists. Please choose another.")
        elif not username:
            print("Username cannot be empty.")
        else:
            break
    password = input("Choose a password: ").strip()
    users[username] = {
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "admin": admin
    }
    save_users(users)
    print(f"\nUser '{username}' registered successfully!" + (" (Admin)" if admin else "") + "\n")
    input("Press Enter to return to the main menu...")