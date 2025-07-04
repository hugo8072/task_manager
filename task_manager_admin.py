"""
Task manager admin module.
Administrative functions for task management system.
Provides admin-specific functionality for user and task management.
"""

from loads import load_tasks, load_users
from statistics_admin import admin_statistics_menu
from search_filter import search_and_filter_menu_admin
from screen_utils import clear_screen, display_last_action, display_full_screen_menu
from colors import Colors, success, error, warning, info, title, border, prompt
from task_manager_user import task_menu
from task_utils import (
    list_unfinished_tasks_for_all_users,
    get_completed_tasks,
    get_pending_tasks,
    display_task_list,
    sort_tasks_by_priority,
    sort_tasks_by_deadline
)

def admin_main_menu():
    """
    Main admin menu: choose between user view or admin view.
    """
    while True:
        menu_items = [
            f"{Colors.GREEN}1. {Colors.WHITE}User View (impersonate any user)",
            f"{Colors.BLUE}2. {Colors.WHITE}Admin View (administrative functions)",
            f"{Colors.RED}0. {Colors.WHITE}Logout"
        ]

        display_full_screen_menu(
            menu_items,
            "Welcome, Admin!",
            "Choose how you want to access the system"
        )

        choice = input(prompt("Choose an option: ")).strip()

        if choice == "1":
            # User view - let admin choose which user to impersonate
            user_impersonation_menu()
        elif choice == "2":
            # Admin view - administrative functions
            admin_menu()
        elif choice == "0":
            clear_screen()
            print(success("Logging out from admin menu..."))
            break
        else:
            print(error("Invalid option. Please choose 0, 1, or 2."))
            input("Press Enter to continue...")

def user_impersonation_menu():
    """
    Let admin choose which user to impersonate.
    """
    users = load_users()

    if not users:
        print(warning("No users found in the system."))
        input("Press Enter to continue...")
        return

    while True:
        clear_screen()
        print(border("=" * 50))
        print(title("        User Impersonation"))
        print(border("=" * 50))
        print(info("Choose a user to view their tasks as:"))
        print()

        # List all users
        user_list = list(users.keys())
        for idx, username in enumerate(user_list, 1):
            admin_badge = " (Admin)" if users[username].get("admin", False) else ""
            print(f"{Colors.CYAN}{idx}. {Colors.WHITE}{username}{admin_badge}")

        print(f"{Colors.RED}0. {Colors.WHITE}Back to main admin menu")
        print(border("=" * 50))

        choice = input(prompt("Choose a user: ")).strip()

        if choice == "0":
            break

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(user_list):
                selected_user = user_list[choice_num - 1]
                print(success(f"Switching to user view for: {selected_user}"))
                input("Press Enter to continue...")
                # Call the user menu with the selected username
                task_menu(selected_user)
            else:
                print(error("Invalid choice. Please select a valid user number."))
                input("Press Enter to continue...")
        except ValueError:
            print(error("Invalid input. Please enter a number."))
            input("Press Enter to continue...")

def list_users():
    """
    List all registered users.
    """
    users = load_users()
    print(title("\n--- Registered Users ---"))
    for idx, username in enumerate(users.keys(), 1):
        admin_badge = " (Admin)" if users[username].get("admin", False) else ""
        print(f"{info(f'{idx}.')} {Colors.WHITE}{username}{admin_badge}")

def list_all_tasks():
    """
    List all tasks for all users.
    """
    users = load_users()
    all_tasks = []

    for username in users:
        tasks = load_tasks(username)

        # Add username to each task for display
        for task in tasks:
            task_copy = task.copy()
            task_copy['username'] = username
            all_tasks.append(task_copy)

    if not all_tasks:
        print(warning("No tasks found for any user."))
        return

    # Use task_utils to display tasks
    display_task_list(all_tasks, "All Tasks", include_user=True)

def list_all_completed_tasks():
    """
    List all completed tasks for all users.
    """
    users = load_users()
    all_completed_tasks = []

    for username in users:
        tasks = load_tasks(username)
        completed_tasks = get_completed_tasks(tasks)

        # Add username to each task for display
        for task in completed_tasks:
            task_copy = task.copy()
            task_copy['username'] = username
            all_completed_tasks.append(task_copy)

    if not all_completed_tasks:
        print(warning("No completed tasks found for any user."))
        return

    # Use task_utils to display tasks
    display_task_list(all_completed_tasks, "All Completed Tasks", include_user=True)

def list_all_pending_tasks():
    """
    List all pending tasks for all users with sorting options.
    """
    users = load_users()
    all_pending_tasks = []

    # Collect all pending tasks from all users
    for username in users:
        tasks = load_tasks(username)
        pending = get_pending_tasks(tasks)
        for task in pending:
            task_with_user = task.copy()
            task_with_user['username'] = username
            all_pending_tasks.append(task_with_user)

    if not all_pending_tasks:
        print(warning("No pending tasks found for any user."))
        return

    print(title("\n--- All Pending Tasks ---"))
    print(f"{Colors.CYAN}Choose sorting option:")
    print(f"{Colors.YELLOW}1. {Colors.WHITE}By Priority (High to Low)")
    print(f"{Colors.YELLOW}2. {Colors.WHITE}By Deadline (Earliest first)")
    print(f"{Colors.YELLOW}3. {Colors.WHITE}By User (Alphabetical)")
    print(f"{Colors.YELLOW}4. {Colors.WHITE}No sorting (by user, original order)")

    choice = input(prompt("Enter your choice (1-4): ")).strip()

    if choice == "1":
        # Sort by priority using task_utils
        all_pending_tasks = sort_tasks_by_priority(all_pending_tasks)
        # Then by username
        all_pending_tasks.sort(key=lambda x: (int(x.get('priority', '3')), x['username']))
        print(info("Sorted by priority (High to Low), then by user"))
    elif choice == "2":
        # Sort by deadline using task_utils
        all_pending_tasks = sort_tasks_by_deadline(all_pending_tasks)
        # Then by username
        all_pending_tasks.sort(key=lambda x: (x.get('deadline', '9999-12-31'), x['username']))
        print(info("Sorted by deadline (Earliest first), then by user"))
    elif choice == "3":
        # Sort by user
        all_pending_tasks.sort(key=lambda x: (x['username'], x.get('deadline', '9999-12-31')))
        print(info("Sorted by user (Alphabetical), then by deadline"))
    elif choice == "4":
        # Group by user, original order
        print(info("Grouped by user, original order"))
        for username in users:
            user_tasks = [task for task in all_pending_tasks if task['username'] == username]
            if user_tasks:
                display_task_list(user_tasks, f"Pending Tasks for {username}", include_user=False)
        return
    else:
        print(warning("Invalid choice, showing grouped by user"))
        choice = "4"

    if choice != "4":
        print()
        # Use task_utils para exibir as tarefas
        display_task_list(all_pending_tasks, "All Pending Tasks", include_user=True)
    # Removed the input here to fix double Enter prompt
def list_all_pending_tasks_old():
    """
    List all pending tasks for all users (original version).
    This is kept for reference but not used anymore.
    Use list_all_pending_tasks() instead which uses task_utils.
    """
    # Function kept as reference only, implementation removed

def admin_menu():
    """
    Simplified admin menu: only administrative functions (no user task management).
    """
    last_action = None
    last_result = None

    while True:
        menu_items = [
            f"{Colors.CYAN}1. {Colors.WHITE}List all users",
            f"{Colors.BLUE}2. {Colors.WHITE}View all tasks (all users)",
            f"{Colors.YELLOW}3. {Colors.WHITE}View all pending tasks (all users)",
            f"{Colors.MAGENTA}4. {Colors.WHITE}View all completed tasks (all users)",
            f"{Colors.RED}5. {Colors.WHITE}View all unfinished tasks (overdue)",
            f"{Colors.GREEN}6. {Colors.WHITE}View statistics (all users)",
            f"{Colors.CYAN}7. {Colors.WHITE}Search & Filter tasks (all users)",
            f"{Colors.RED}0. {Colors.WHITE}Back to main menu"
        ]

        display_full_screen_menu(
            menu_items,
            "Admin Management",
            "Administrative Functions"
        )

        # Display last action if available
        if last_action and last_result:
            display_last_action(last_action, last_result)

        choice = input(prompt("Choose an option: ")).strip()

        try:
            if choice == "1":
                last_action = info("List all users")
                list_users()
                input(f"\n{Colors.CYAN}Press Enter to continue...")
                last_result = success("Users list displayed")

            elif choice == "2":
                last_action = info("View all tasks")
                list_all_tasks()
                input(f"\n{Colors.CYAN}Press Enter to continue...")
                last_result = success("All tasks from all users displayed")

            elif choice == "3":
                last_action = info("View all pending tasks")
                list_all_pending_tasks()
                input(f"\n{Colors.CYAN}Press Enter to continue...")
                last_result = success("All pending tasks from all users displayed")

            elif choice == "4":
                last_action = info("View all completed tasks")
                list_all_completed_tasks()
                input(f"\n{Colors.CYAN}Press Enter to continue...")
                last_result = success("All completed tasks from all users displayed")

            elif choice == "5":
                last_action = info("View all unfinished tasks")
                list_unfinished_tasks_for_all_users()
                input(f"\n{Colors.CYAN}Press Enter to continue...")
                last_result = success("All unfinished tasks from all users displayed")

            elif choice == "6":
                last_action = info("View statistics")
                admin_statistics_menu()
                last_result = success("Statistics menu accessed")

            elif choice == "7":
                last_action = info("Search & filter tasks")
                search_and_filter_menu_admin()
                last_result = success("Search & filter menu accessed")

            elif choice == "0":
                break

            else:
                last_action = error(f"Invalid option: {choice}")
                last_result = error("Please choose a valid option (0-7)")
                print(f"\n{last_result}")
                input(f"\n{Colors.CYAN}Press Enter to continue...")

        except (KeyError, FileNotFoundError, ValueError) as e:
            last_action = error(f"Error in option {choice}")
            last_result = error(f"An error occurred: {str(e)}")
            print(f"\n{last_result}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
