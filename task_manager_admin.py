from loads import load_tasks, load_users

def list_users():
    """
    List all registered users.
    """
    users = load_users()
    print("\n--- Registered Users ---")
    for idx, username in enumerate(users.keys(), 1):
        print(f"{idx}. {username}")

def list_tasks_user(username):
    """
    List all tasks for a specific user (admin view).
    """
    print(f"\n--- Task List for {username} ---")
    tasks = load_tasks(username)
    found = False
    for idx, task in enumerate(tasks):
        status = "Done" if task.get("completed", False) else "Pending"
        print(f"{idx+1}. {task['title']} | {task['description']} | Priority: {task['priority']} | Deadline: {task['deadline']} | Category: {task['category']} | Status: {status}")
        found = True
    if not found:
        print("No tasks found.")

def list_all_tasks():
    """
    List all tasks for all users.
    """
    users = load_users()
    for username in users:
        list_tasks_user(username)

def admin_menu():
    """
    Admin menu: view tasks by user or all users.
    """

    users = load_users()


    while True:
        print("\n--- Admin Task View Menu ---")
        print("1. List all users")
        print("2. View tasks of a specific user")
        print("3. View all tasks (all users)")
        print("0. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_users()
        elif choice == "2":
            username = input("Enter username: ").strip()
            if username in users:
                list_tasks_user(username)
            else:
                print("User not found.")
        elif choice == "3":
            list_all_tasks()
        elif choice == "0":
            print("Logging out from admin menu...")
            break
        else:
            print("Invalid option. Try again.")