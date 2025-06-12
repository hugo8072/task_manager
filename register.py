import hashlib
from saves import save_users

def register(users):
    """
    Handle the user registration process, including username and password validation.
    This function checks if the username already exists and prompts for a new one if it does.
    It hashes the password using SHA-256 before saving it to the users dictionary.
    It saves the updated users dictionary to the users JSON file.
    """
    print("=" * 40)
    print("           Register Page")
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
    users[username] = hashlib.sha256(password.encode()).hexdigest()
    save_users(users)
    print(f"\nUser '{username}' registered successfully!\n")
    input("Press Enter to return to the main menu...")    