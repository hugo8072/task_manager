"""
Administrative statistics module.

This module provides statistical analysis functionality for all users
in the system, including task counts, completion rates, and category analysis.
"""

from loads import load_users
from task_utils import (
    display_global_statistics,
    list_unfinished_tasks_for_all_users,
    get_user_tasks,
    calculate_completion_rate,
    get_category_counts,
    get_top_categories
)
from screen_utils import clear_screen, display_last_action
from colors import Colors, success, error, warning, info, title, border, prompt


def total_tasks_per_user():
    """
    Print total number of tasks per user.

    Uses a simple iteration through users to count their tasks.
    """
    users = load_users()
    print(title("\n--- Total Number of Tasks Per User ---"))

    if not users:
        print(warning("No users found in the system."))
        return

    for username in users:
        tasks = get_user_tasks(username)
        print(f"{Colors.CYAN}{username}: {Colors.WHITE}{len(tasks)} {info('task(s)')}")


def percentage_completed_per_user():
    """
    Print percentage of completed tasks per user.

    Calculates completion rate using generator expression for efficiency.
    """
    users = load_users()
    print(title("\n--- Percentage of Completed Tasks Per User ---"))
    for username in users:
        tasks = get_user_tasks(username)
        total = len(tasks)
        percent = calculate_completion_rate(tasks)
        completed = sum(1 for task in tasks if task.get("completed", False))
        percent_color = success if percent >= 80 else warning if percent >= 50 else error
        print(
            f"{Colors.CYAN}{username}: {percent_color(f'{percent:.2f}%')} completed "
            f"({Colors.GREEN}{completed}/{Colors.BLUE}{total})"
        )


def tasks_per_category():
    """
    Print number of tasks per category using sets.

    Counts total tasks in each category across all users and displays sorted.
    """
    users = load_users()
    category_counts = {}

    # Count tasks per category across all users
    for username in users:
        tasks = get_user_tasks(username)
        user_category_counts = get_category_counts(tasks)
        for category, count in user_category_counts.items():
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += count

    # Display results sorted by category name
    print(title("\n--- Number of Tasks Per Category ---"))
    if category_counts:
        for category in sorted(category_counts.keys()):
            count = category_counts[category]
            print(f"{Colors.MAGENTA}{category}: {Colors.WHITE}{count} {info('task(s)')}")
    else:
        print(warning("No categories found."))


def most_used_categories():
    """
    Print the top 3 most frequently used categories.

    Uses list comprehension and Counter to find top categories with highest usage.
    """
    users = load_users()
    all_tasks = []

    # Collect all tasks
    for username in users:
        all_tasks.extend(get_user_tasks(username))

    # Get top categories
    top_categories = get_top_categories(all_tasks, 3)

    if not top_categories:
        print(warning("\nNo categories found."))
        return

    # Get top 3 most used categories
    print(title("\n--- Top 3 Most Used Categories ---"))
    for idx, (category, count) in enumerate(top_categories, 1):
        rank_color = Colors.YELLOW if idx == 1 else Colors.GREEN if idx == 2 else Colors.BLUE
        task_text = info('task(s)')
        print(f"{rank_color}{idx}. {Colors.MAGENTA}{category}: "
              f"{Colors.WHITE}{count} {task_text}")

    # If less than 3 categories exist, mention it
    if len(top_categories) < 3:
        print(warning(f"\nNote: Only {len(top_categories)} "
                      f"categor{'y' if len(top_categories) == 1 else 'ies'} found in the system."))


def display_global_stats():
    """
    Display comprehensive global statistics for all users.
    """
    display_global_statistics()


def admin_statistics_menu():
    """
    Display and handle the administrative statistics menu.

    Provides options to view various statistics across all users.
    """
    last_command = ""
    last_result = ""

    while True:
        clear_screen()
        if last_command and last_result:
            display_last_action(last_command, last_result)

        print(border("=" * 50))
        print(title("        Admin Statistics"))
        print(border("=" * 50))
        print(title("\n--- Statistics Menu ---"))
        print(f"{Colors.GREEN}1. {Colors.WHITE}Total tasks per user")
        print(f"{Colors.BLUE}2. {Colors.WHITE}Task completion percentage per user")
        print(f"{Colors.MAGENTA}3. {Colors.WHITE}Number of tasks per category")
        print(f"{Colors.YELLOW}4. {Colors.WHITE}Top 3 most used categories")
        print(f"{Colors.CYAN}5. {Colors.WHITE}View all unfinished tasks")
        print(f"{Colors.GREEN}6. {Colors.WHITE}Global statistics overview")
        print(f"{Colors.RED}0. {Colors.WHITE}Back")

        choice = input(prompt("Choose an option: ")).strip()

        if choice == "1":
            total_tasks_per_user()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("Total tasks per user")
            last_result = success("Statistics displayed successfully")

        elif choice == "2":
            percentage_completed_per_user()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("Task completion percentage per user")
            last_result = success("Statistics displayed successfully")

        elif choice == "3":
            tasks_per_category()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("Number of tasks per category")
            last_result = success("Statistics displayed successfully")

        elif choice == "4":
            most_used_categories()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("Top 3 most used categories")
            last_result = success("Top categories displayed successfully")

        elif choice == "5":
            list_unfinished_tasks_for_all_users()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("View all unfinished tasks")
            last_result = success("Unfinished tasks displayed successfully")

        elif choice == "6":
            display_global_stats()
            input(f"\n{Colors.CYAN}Press Enter to continue...")
            last_command = success("Global statistics overview")
            last_result = success("Global statistics displayed successfully")

        elif choice == "0":
            break
        else:
            last_command = error(f"Invalid option: {choice}")
            last_result = error("Please choose a valid option")
            print(f"\n{last_result}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")


# For direct testing
if __name__ == "__main__":
    admin_statistics_menu()
