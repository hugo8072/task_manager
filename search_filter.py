"""
Search and filter module for task management.
Provides search and filtering functionality for tasks by various criteria.
"""

from loads import load_tasks, load_users
from screen_utils import clear_screen, display_last_action
from colors import Colors, success, error, warning, info, title, border, prompt


# ===== USER SEARCH FUNCTIONS =====

def search_tasks_by_priority(username, priority):
    """
    Search tasks by priority for a specific user using list comprehension.

    Args:
        username (str): The username to search tasks for.
        priority (str): Priority to filter by ("1", "2", or "3").

    Returns:
        list: Filtered tasks matching the priority.
    """
    tasks = load_tasks(username)
    # List comprehension to filter by priority
    filtered_tasks = [
        task for task in tasks
        if task.get("priority", "") == priority
    ]
    return filtered_tasks


def search_tasks_by_category(username, category):
    """
    Search tasks by category for a specific user using list comprehension.

    Args:
        username (str): The username to search tasks for.
        category (str): Category to filter by.

    Returns:
        list: Filtered tasks matching the category.
    """
    tasks = load_tasks(username)
    # List comprehension to filter by category (case-insensitive)
    filtered_tasks = [
        task for task in tasks
        if task.get("category", "").lower() == category.lower()
    ]
    return filtered_tasks


def search_tasks_by_date_range(username, start_date, end_date):
    """
    Search tasks by date range for a specific user using list comprehension.

    Args:
        username (str): The username to search tasks for.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        list: Filtered tasks within the date range.
    """
    tasks = load_tasks(username)

    # List comprehension to filter by date range (dates already in YYYY-MM-DD format)
    filtered_tasks = [
        task for task in tasks
        if start_date  <= end_date
    ]
    return filtered_tasks


def display_filtered_tasks(tasks, filter_type, filter_value):
    """
    Display filtered tasks in a formatted way.

    Args:
        tasks (list): List of filtered tasks.
        filter_type (str): Type of filter applied.
        filter_value (str): Value used for filtering.
    """
    print(title(f"\n--- Tasks filtered by {filter_type}: {filter_value} ---"))
    if not tasks:
        print(warning("No tasks found matching the criteria."))
        return

    for idx, task in enumerate(tasks, 1):
        status = success("Done") if task.get("completed", False) else warning("Pending")
        priority = task.get('priority', 'N/A')
        if priority == "1":
            priority_color = Colors.RED
        elif priority == "2":
            priority_color = Colors.YELLOW
        else:
            priority_color = Colors.GREEN
        print(f"{info(f'{idx}.')} {Colors.WHITE}{task.get('title', 'Untitled')} | "
              f"Priority: {priority_color}{priority} | "
              f"Deadline: {Colors.CYAN}{task.get('deadline', 'N/A')} | "
              f"Category: {Colors.MAGENTA}{task.get('category', 'N/A')} | "
              f"Status: {status}")
        if task.get('description'):
            print(f"   {Colors.DIM}Description: {task['description']}")


def search_and_filter_menu(username):
    """
    Menu for searching and filtering tasks using list comprehensions.

    Args:
        username (str): The username to search tasks for.
    """
    last_action = None
    last_result = None

    while True:
        clear_screen()
        print(border("=" * 50))
        print(title(f"        Search & Filter - {username}"))
        print(border("=" * 50))

        # Display last action if available
        if last_action and last_result:
            display_last_action(last_action, last_result)

        print(title("\n--- Search & Filter Menu ---"))
        print(f"{Colors.GREEN}1. {Colors.WHITE}Search by priority")
        print(f"{Colors.BLUE}2. {Colors.WHITE}Search by category")
        print(f"{Colors.YELLOW}3. {Colors.WHITE}Search by date range")
        print(f"{Colors.RED}0. {Colors.WHITE}Back to main menu")

        choice = input(prompt("Choose an option: ")).strip()

        try:
            if choice == "1":
                last_action = info("Search by priority")
                print(f"\n{Colors.CYAN}Priority options: 1=High, 2=Medium, 3=Low")
                priority = input(prompt("Enter priority (1, 2, or 3): ")).strip()
                if priority in ["1", "2", "3"]:
                    filtered_tasks = search_tasks_by_priority(username, priority)
                    priority_names = {"1": "High", "2": "Medium", "3": "Low"}
                    display_filtered_tasks(filtered_tasks, "priority",
                                         f"{priority} ({priority_names[priority]})")
                    priority_name = priority_names[priority]
                    last_result = success(f"Found {len(filtered_tasks)} tasks "
                                        f"with priority {priority_name}")
                else:
                    last_result = error("Invalid priority. Please enter 1, 2, or 3.")
                    print(f"\n{last_result}")

            elif choice == "2":
                last_action = info("Search by category")
                category = input(prompt("Enter category to search for: ")).strip()
                if category:
                    filtered_tasks = search_tasks_by_category(username, category)
                    display_filtered_tasks(filtered_tasks, "category", category)
                    last_result = success(f"Found {len(filtered_tasks)} tasks "
                                        f"in category '{category}'")
                else:
                    last_result = error("Category cannot be empty.")
                    print(f"\n{last_result}")

            elif choice == "3":
                last_action = info("Search by date range")
                print(f"{Colors.CYAN}Enter date range (YYYY-MM-DD format)")
                start_date = input(prompt("Start date: ")).strip()
                end_date = input(prompt("End date: ")).strip()

                # Basic validation
                if (len(start_date) == 10 and len(end_date) == 10 and
                    start_date[4] == '-' and start_date[7] == '-' and
                    end_date[4] == '-' and end_date[7] == '-'):
                    filtered_tasks = search_tasks_by_date_range(username, start_date, end_date)
                    display_filtered_tasks(filtered_tasks, "date range",
                                         f"{start_date} to {end_date}")
                    last_result = success(f"Found {len(filtered_tasks)} tasks in date range")
                else:
                    last_result = error("Invalid date format. Please use YYYY-MM-DD format.")
                    print(f"\n{last_result}")

            elif choice == "0":
                break
            else:
                last_action = error(f"Invalid option: {choice}")
                last_result = error("Invalid option. Try again.")
                print(f"\n{last_result}")

            # Wait for user before clearing screen (except for back)
            if choice != "0":
                input(f"\n{Colors.CYAN}Press Enter to continue...")

        except (ValueError, TypeError, KeyError, FileNotFoundError) as e:
            last_action = error(f"Error in option {choice}")
            last_result = error(f"An error occurred: {str(e)}")
            print(f"\n{last_result}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")


# ===== ADMIN SEARCH FUNCTIONS =====

def search_tasks_by_priority_admin(priority):
    """
    Search tasks by priority across all users using list comprehension.

    Args:
        priority (str): Priority to filter by ("1", "2", or "3").

    Returns:
        list: Filtered tasks with username information.
    """
    users = load_users()
    all_filtered_tasks = []

    # List comprehension to collect all tasks with priority across users
    for username in users:
        tasks = load_tasks(username)
        filtered_tasks = [
            {**task, 'username': username} for task in tasks
            if task.get("priority", "") == priority
        ]
        all_filtered_tasks.extend(filtered_tasks)

    return all_filtered_tasks


def search_tasks_by_category_admin(category):
    """
    Search tasks by category across all users using list comprehension.

    Args:
        category (str): Category to filter by.

    Returns:
        list: Filtered tasks with username information.
    """
    users = load_users()
    all_filtered_tasks = []

    # List comprehension to collect all tasks with category across users
    for username in users:
        tasks = load_tasks(username)
        filtered_tasks = [
            {**task, 'username': username} for task in tasks
            if task.get("category", "").lower() == category.lower()
        ]
        all_filtered_tasks.extend(filtered_tasks)

    return all_filtered_tasks


def search_tasks_by_date_range_admin(start_date, end_date):
    """
    Search tasks by date range across all users using list comprehension.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        list: Filtered tasks with username information.
    """
    users = load_users()
    all_filtered_tasks = []

    # List comprehension to collect all tasks within date range across users
    for username in users:
        tasks = load_tasks(username)
        filtered_tasks = [
            {**task, 'username': username} for task in tasks
            if start_date <= task.get("deadline", "") <= end_date
        ]
        all_filtered_tasks.extend(filtered_tasks)

    return all_filtered_tasks


def display_filtered_tasks_admin(tasks, filter_type, filter_value):
    """
    Display filtered tasks in a formatted way for admin view.

    Args:
        tasks (list): List of filtered tasks with username info.
        filter_type (str): Type of filter applied.
        filter_value (str): Value used for filtering.
    """
    print(title(f"\n--- All tasks filtered by {filter_type}: {filter_value} ---"))
    if not tasks:
        print(warning("No tasks found matching the criteria."))
        return

    for idx, task in enumerate(tasks, 1):
        status = success("Done") if task.get("completed", False) else warning("Pending")
        priority = task.get('priority', 'N/A')
        if priority == "1":
            priority_color = Colors.RED
        elif priority == "2":
            priority_color = Colors.YELLOW
        else:
            priority_color = Colors.GREEN
        username_color = Colors.CYAN
        username = task.get('username', 'Unknown')
        task_title = task.get('title', 'Untitled')
        print(f"{info(f'{idx}.')} [{username_color}{username}] "
              f"{Colors.WHITE}{task_title} | "
              f"Priority: {priority_color}{priority} | "
              f"Deadline: {Colors.CYAN}{task.get('deadline', 'N/A')} | "
              f"Category: {Colors.MAGENTA}{task.get('category', 'N/A')} | "
              f"Status: {status}")
        if task.get('description'):
            print(f"   {Colors.DIM}Description: {task['description']}")


def search_and_filter_menu_admin():
    """
    Admin menu for searching and filtering tasks across all users with screen management.
    """
    last_action = None
    last_result = None

    while True:
        clear_screen()
        print(border("=" * 50))
        print(title("        Admin Search & Filter"))
        print(border("=" * 50))

        # Display last action if available
        if last_action and last_result:
            display_last_action(last_action, last_result)

        print(title("\n--- Admin Search & Filter Menu ---"))
        print(f"{Colors.GREEN}1. {Colors.WHITE}Search by priority (all users)")
        print(f"{Colors.BLUE}2. {Colors.WHITE}Search by category (all users)")
        print(f"{Colors.YELLOW}3. {Colors.WHITE}Search by date range (all users)")
        print(f"{Colors.RED}0. {Colors.WHITE}Back to admin menu")

        choice = input(prompt("Choose an option: ")).strip()

        try:
            if choice == "1":
                last_action = info("Search by priority")
                print(f"\n{Colors.CYAN}Priority options: 1=High, 2=Medium, 3=Low")
                priority = input(prompt("Enter priority (1, 2, or 3): ")).strip()
                if priority in ["1", "2", "3"]:
                    filtered_tasks = search_tasks_by_priority_admin(priority)
                    priority_names = {"1": "High", "2": "Medium", "3": "Low"}
                    display_filtered_tasks_admin(filtered_tasks, "priority",
                                               f"{priority} ({priority_names[priority]})")
                    priority_name = priority_names[priority]
                    last_result = success(f"Found {len(filtered_tasks)} tasks "
                                        f"with priority {priority_name}")
                else:
                    last_result = error("Invalid priority entered")
                    print(f"\n{last_result}")

            elif choice == "2":
                last_action = info("Search by category")
                category = input(prompt("Enter category to search for: ")).strip()
                if category:
                    filtered_tasks = search_tasks_by_category_admin(category)
                    display_filtered_tasks_admin(filtered_tasks, "category", category)
                    last_result = success(f"Found {len(filtered_tasks)} tasks "
                                        f"in category '{category}'")
                else:
                    last_result = error("No category provided")
                    print(f"\n{last_result}")

            elif choice == "3":
                last_action = info("Search by date range")
                print(f"{Colors.CYAN}Enter date range (YYYY-MM-DD format)")
                start_date = input(prompt("Start date: ")).strip()
                end_date = input(prompt("End date: ")).strip()

                # Basic validation
                if (len(start_date) == 10 and len(end_date) == 10 and
                    start_date[4] == '-' and start_date[7] == '-' and
                    end_date[4] == '-' and end_date[7] == '-'):
                    filtered_tasks = search_tasks_by_date_range_admin(start_date, end_date)
                    display_filtered_tasks_admin(filtered_tasks, "date range",
                                               f"{start_date} to {end_date}")
                    last_result = success(f"Found {len(filtered_tasks)} tasks in date range")
                else:
                    last_result = error("Invalid date format provided")
                    print(f"\n{last_result}")

            elif choice == "0":
                break

            else:
                last_action = error(f"Invalid option: {choice}")
                last_result = error("Please choose a valid option (0-3)")
                print(f"\n{last_result}")

            # Wait for user before clearing screen (except for back)
            if choice != "0":
                input(f"\n{Colors.CYAN}Press Enter to continue...")

        except (ValueError, TypeError, KeyError, FileNotFoundError) as e:
            last_action = error(f"Error in option {choice}")
            last_result = error(f"An error occurred: {str(e)}")
            print(f"\n{last_result}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
