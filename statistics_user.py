"""
User-specific statistics module.

This module implements functionality to calculate and display statistics
for a user's tasks, using task_utils for code reuse.
"""

from loads import load_tasks
from task_utils import (
    display_user_statistics as task_utils_display_stats,
    list_unfinished_tasks_for_user,
    calculate_completion_rate,
    get_all_categories,
    get_category_counts,
    get_top_categories
)
from screen_utils import clear_screen, display_last_action
from search_filter import search_and_filter_menu
from colors import Colors, success, error, warning, info, title, border, prompt


def get_total_tasks(username):
    """
    Get the total number of tasks for a specific user.

    Args:
        username (str): The username to get task count for.

    Returns:
        int: Total number of tasks for the user.
    """
    tasks = load_tasks(username)
    return len(tasks)


def get_completion_percentage(username):
    """
    Calculate the percentage of completed tasks for a specific user.

    Args:
        username (str): The username to calculate completion percentage for.

    Returns:
        float: Percentage of completed tasks (0-100).
    """
    tasks = load_tasks(username)
    return calculate_completion_rate(tasks)


def get_unique_categories(username):
    """
    Get unique categories from all tasks using sets.

    Args:
        username (str): The username to get unique categories for.

    Returns:
        set: Set of unique categories.
    """
    tasks = load_tasks(username)
    # Convert list to set for consistent return type with old function
    return set(get_all_categories(tasks))


def get_tasks_per_category(username):
    """
    Get number of tasks per category for a specific user.

    Args:
        username (str): The username to analyze categories for.

    Returns:
        dict: Dictionary with categories as keys and task counts as values.
    """
    tasks = load_tasks(username)
    return get_category_counts(tasks)


def get_most_used_categories(username):
    """
    Get the top 3 most used categories and their counts.

    Args:
        username (str): The username to analyze categories for.

    Returns:
        list: List of tuples (category, count) sorted by count in
              descending order, limited to top 3.
    """
    tasks = load_tasks(username)
    return get_top_categories(tasks, 3)


def display_user_statistics(username):
    """
    Display comprehensive statistics for a specific user.

    Args:
        username (str): The username to display statistics for.
    """
    # Use the function from task_utils
    task_utils_display_stats(username)


def user_statistics_menu(username):
    """
    Menu for user-specific statistics.

    Args:
        username (str): The username to display statistics for.
    """
    last_command = ""
    last_result = ""

    while True:
        clear_screen()
        if last_command and last_result:
            display_last_action(last_command, last_result)

        print(border("=" * 50))
        print(title(f"        Statistics - {username}"))
        print(border("=" * 50))
        print(title(f"\n--- Statistics Menu - {username} ---"))
        print(f"{Colors.CYAN}1. {Colors.WHITE}View all statistics")
        print(f"{Colors.GREEN}2. {Colors.WHITE}Total number of tasks")
        print(f"{Colors.BLUE}3. {Colors.WHITE}Tasks completion percentage")
        print(f"{Colors.MAGENTA}4. {Colors.WHITE}Unique categories")
        print(f"{Colors.YELLOW}5. {Colors.WHITE}Number of tasks per category")
        print(f"{Colors.CYAN}6. {Colors.WHITE}Top 3 most used categories")
        print(f"{Colors.GREEN}7. {Colors.WHITE}View unfinished tasks")
        print(f"{Colors.BLUE}8. {Colors.WHITE}Search & Filter tasks")
        print(f"{Colors.RED}0. {Colors.WHITE}Back to task manager menu")

        choice = input(prompt("Choose an option: ")).strip()

        if choice == "1":
            display_user_statistics(username)
            last_command = success("View all statistics")
            last_result = success("All statistics displayed successfully")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "2":
            total = get_total_tasks(username)
            print(f"\n{Colors.WHITE}Total number of tasks: {Colors.CYAN}{total}")
            last_command = success("Total number of tasks")
            last_result = success(f"Found {total} tasks")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "3":
            percentage = get_completion_percentage(username)
            percent_color = success if percentage >= 80 else warning if percentage >= 50 else error
            print(f"\n{Colors.WHITE}Tasks completion percentage:"
                  f"{percent_color(f'{percentage:.1f}%')}")
            last_command = success("Tasks completion percentage")
            last_result = success(f"Completion rate: {percentage:.1f}%")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "4":
            categories = get_unique_categories(username)
            print(f"\n{Colors.WHITE}Unique categories "
                  f"({Colors.CYAN}{len(categories)}{Colors.WHITE}):")
            for category in sorted(categories):
                print(f"  {Colors.MAGENTA}• {Colors.WHITE}{category}")
            last_command = success("Unique categories")
            last_result = success(f"Found {len(categories)} unique categories")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "5":
            tasks_per_category = get_tasks_per_category(username)
            total_tasks = get_total_tasks(username)
            if tasks_per_category:
                print(info("\nNumber of tasks per category:"))
                for category in sorted(tasks_per_category.keys()):
                    count = tasks_per_category[category]
                    percentage = (count / total_tasks) * 100 if total_tasks > 0 else 0
                    print(f"  {Colors.MAGENTA}• {Colors.WHITE}{category}: "
                          f"{Colors.CYAN}{count} task(s) ({Colors.YELLOW}{percentage:.1f}%)")
                last_command = success("Number of tasks per category")
                last_result = success(f"Displayed tasks for {len(tasks_per_category)} categories")
            else:
                print(warning("\nNo categories found."))
                last_command = warning("Number of tasks per category")
                last_result = warning("No categories found")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "6":
            most_used = get_most_used_categories(username)
            total_tasks = get_total_tasks(username)
            if most_used:
                print(info("\nTop 3 most used categories:"))
                for idx, (category, count) in enumerate(most_used, 1):
                    percentage = (
                        (count / total_tasks) * 100
                        if total_tasks > 0
                        else 0
                    )
                    rank_color = (Colors.YELLOW if idx == 1
                                 else Colors.GREEN if idx == 2
                                 else Colors.BLUE)
                    print(f"  {rank_color}{idx}. {Colors.WHITE}{category}: "
                          f"{Colors.CYAN}{count} task(s) "
                          f"({Colors.YELLOW}{percentage:.1f}%)")

                # If less than 3 categories exist, mention it
                if len(most_used) < 3:
                    category_word = 'y' if len(most_used) == 1 else 'ies'
                    print(warning(f"  Note: Only {len(most_used)} "
                                 f"categor{category_word} found."))

                last_command = success("Top 3 most used categories")
                last_result = success(f"Displayed top {len(most_used)} categories")
            else:
                print(warning("\nNo categories found."))
                last_command = warning("Top 3 most used categories")
                last_result = warning("No categories found")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "7":
            last_command = info("View unfinished tasks")
            list_unfinished_tasks_for_user(username)
            last_result = success("Unfinished tasks displayed")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
        elif choice == "8":
            last_command = info("Search & Filter tasks")
            search_and_filter_menu(username)
            last_result = success("Search & filter menu accessed")
            # No input needed here as search menu handles its own pauses
        elif choice == "0":
            break
        else:
            last_command = error(f"Invalid option: {choice}")
            last_result = error("Please choose a valid option")
            print(f"\n{last_result}")
            input(f"\n{Colors.CYAN}Press Enter to continue...")
