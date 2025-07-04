"""
Task utilities module.
Common functions for task management and statistics.
"""

from collections import Counter
from datetime import datetime

from colors import Colors, success, warning, info, title, prompt
from loads import load_tasks, load_users


def get_user_tasks(username):
    """Get all tasks for a specific user."""
    return load_tasks(username)


def get_all_users_tasks():
    """Get all tasks for all users as a dict {username: tasks}."""
    users = load_users()
    return {username: load_tasks(username) for username in users}


def get_completed_tasks(tasks):
    """Filter completed tasks from a task list."""
    return [task for task in tasks if task.get("completed", False)]


def get_pending_tasks(tasks):
    """Filter pending tasks from a task list."""
    return [task for task in tasks if not task.get("completed", False)]


def get_overdue_tasks(tasks):
    """Filter overdue tasks (pending tasks past their deadline)."""
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        task for task in tasks
        if not task.get("completed", False) and task.get("deadline", "9999-12-31") < today
    ]


def get_unfinished_tasks(tasks):
    """Filter unfinished tasks (pending tasks that are overdue)."""
    return get_overdue_tasks(tasks)


def get_tasks_by_priority(tasks, priority):
    """Filter tasks by priority level."""
    return [task for task in tasks if task.get("priority", "3") == str(priority)]


def get_tasks_by_category(tasks, category):
    """Filter tasks by category."""
    return [task for task in tasks if task.get("category", "").lower() == category.lower()]


def calculate_completion_rate(tasks):
    """Calculate completion rate as percentage."""
    if not tasks:
        return 0.0
    completed = len(get_completed_tasks(tasks))
    return (completed / len(tasks)) * 100


def get_all_categories(tasks):
    """Get all unique categories from tasks."""
    return list(set(task.get("category", "Uncategorized") for task in tasks))


def get_category_counts(tasks):
    """Get count of tasks per category."""
    categories = {}
    for task in tasks:
        category = task.get("category", "Uncategorized")
        categories[category] = categories.get(category, 0) + 1
    return categories


def get_top_categories(tasks, limit=3):
    """Get top N most used categories."""
    categories = [task.get("category", "Uncategorized") for task in tasks]
    counter = Counter(categories)
    return counter.most_common(limit)


def sort_tasks_by_priority(tasks):
    """Sort tasks by priority (1=High, 2=Medium, 3=Low)."""
    return sorted(tasks, key=lambda x: int(x.get('priority', '3')))


def sort_tasks_by_deadline(tasks):
    """Sort tasks by deadline (earliest first)."""
    return sorted(tasks, key=lambda x: x.get('deadline', '9999-12-31'))


def display_task_summary(task, include_user=False, task_number=None):
    """Display a formatted task summary."""
    status = success("Done") if task.get("completed", False) else warning("Pending")

    # Determine priority color
    if task['priority'] == "1":
        priority_color = Colors.RED
    elif task['priority'] == "2":
        priority_color = Colors.YELLOW
    else:
        priority_color = Colors.GREEN

    prefix = f"{info(f'{task_number}.')}" if task_number else ""
    user_info = ""
    if include_user and 'username' in task:
        user_info = f"[{Colors.MAGENTA}{task['username']}{Colors.WHITE}] "

    # Build task display string in parts
    task_info = (f"{prefix} {user_info}{Colors.WHITE}{task['title']} | "
                 f"{task['description']} | Priority: {priority_color}{task['priority']} | "
                 f"Deadline: {Colors.CYAN}{task['deadline']} | "
                 f"Category: {Colors.MAGENTA}{task['category']} | Status: {status}")

    print(task_info)


def display_task_list(tasks, title_text, include_user=False, numbered=True):
    """Display a formatted list of tasks."""
    print(title(f"\n--- {title_text} ---"))

    if not tasks:
        print(warning("No tasks found."))
        return

    for idx, task in enumerate(tasks, 1):
        task_number = idx if numbered else None
        display_task_summary(task, include_user, task_number)


# Statistics functions for code reuse
def calculate_user_stats(username):
    """Calculate comprehensive statistics for a user."""
    tasks = get_user_tasks(username)
    return {
        'total_tasks': len(tasks),
        'completed_tasks': len(get_completed_tasks(tasks)),
        'pending_tasks': len(get_pending_tasks(tasks)),
        'overdue_tasks': len(get_overdue_tasks(tasks)),
        'completion_rate': calculate_completion_rate(tasks),
        'unique_categories': len(get_all_categories(tasks)),
        'category_counts': get_category_counts(tasks),
        'top_categories': get_top_categories(tasks, 3)
    }


def calculate_global_stats():
    """Calculate comprehensive statistics for all users."""
    users = load_users()
    all_tasks = []
    user_stats = {}

    for username in users:
        user_tasks = get_user_tasks(username)
        all_tasks.extend(user_tasks)
        user_stats[username] = calculate_user_stats(username)

    return {
        'total_users': len(users),
        'total_tasks': len(all_tasks),
        'completed_tasks': len(get_completed_tasks(all_tasks)),
        'pending_tasks': len(get_pending_tasks(all_tasks)),
        'overdue_tasks': len(get_overdue_tasks(all_tasks)),
        'completion_rate': calculate_completion_rate(all_tasks),
        'unique_categories': len(get_all_categories(all_tasks)),
        'category_counts': get_category_counts(all_tasks),
        'top_categories': get_top_categories(all_tasks, 3),
        'user_stats': user_stats
    }


def display_user_statistics(username):
    """Display statistics for a specific user using common functions."""
    stats = calculate_user_stats(username)

    print(title(f"\n--- Statistics for {username} ---"))

    if stats['total_tasks'] == 0:
        print(warning("No tasks found for this user."))
        return

    # Basic stats
    total_tasks = stats['total_tasks']
    print(f"{Colors.WHITE}Total number of tasks:{Colors.RESET} "
          f"{Colors.CYAN}{total_tasks}{Colors.RESET}")

    # Completion rate with color coding
    rate = stats['completion_rate']
    rate_color = success if rate >= 80 else warning if rate >= 50 else Colors.RED
    print(f"{Colors.WHITE}Tasks completion percentage:{Colors.RESET} "
          f"{rate_color}{rate:.1f}%{Colors.RESET}")

    # Task status breakdown
    completed = stats['completed_tasks']
    pending = stats['pending_tasks']
    overdue = stats['overdue_tasks']

    print(f"{Colors.WHITE}Completed tasks:{Colors.RESET} "
          f"{Colors.GREEN}{completed}{Colors.RESET}")
    print(f"{Colors.WHITE}Pending tasks:{Colors.RESET} "
          f"{Colors.YELLOW}{pending}{Colors.RESET}")
    print(f"{Colors.WHITE}Overdue tasks:{Colors.RESET} "
          f"{Colors.RED}{overdue}{Colors.RESET}")

    # Category stats
    unique_categories = stats['unique_categories']
    print(f"{Colors.WHITE}Number of unique categories:{Colors.RESET} "
          f"{Colors.CYAN}{unique_categories}{Colors.RESET}")

    if stats['category_counts']:
        print(info("\nTasks per category:"))
        for category in sorted(stats['category_counts'].keys()):
            count = stats['category_counts'][category]
            percentage = (count / stats['total_tasks']) * 100
            print(f"  {Colors.MAGENTA}• {Colors.WHITE}{category}: "
                  f"{Colors.CYAN}{count} task(s) "
                  f"({Colors.YELLOW}{percentage:.1f}%)")

    # Top categories
    if stats['top_categories']:
        print(info("\nTop 3 categories:"))
        for idx, (category, count) in enumerate(stats['top_categories'], 1):
            rank_color = Colors.YELLOW if idx == 1 else Colors.GREEN if idx == 2 else Colors.BLUE
            print(f"  {rank_color}{idx}. {Colors.MAGENTA}{category}: {Colors.WHITE}{count} task(s)")


def display_global_statistics():
    """Display global statistics using common functions."""
    stats = calculate_global_stats()

    print(title("\n--- Global Statistics ---"))

    # Overall stats
    print(f"{Colors.WHITE}Total users:{Colors.RESET} "
          f"{Colors.CYAN}{stats['total_users']}{Colors.RESET}")
    print(f"{Colors.WHITE}Total tasks:{Colors.RESET} "
          f"{Colors.CYAN}{stats['total_tasks']}{Colors.RESET}")
    print(f"{Colors.WHITE}Completed tasks:{Colors.RESET} "
          f"{Colors.GREEN}{stats['completed_tasks']}{Colors.RESET}")
    print(f"{Colors.WHITE}Pending tasks:{Colors.RESET} "
          f"{Colors.YELLOW}{stats['pending_tasks']}{Colors.RESET}")
    print(f"{Colors.WHITE}Overdue tasks:{Colors.RESET} "
          f"{Colors.RED}{stats['overdue_tasks']}{Colors.RESET}")

    # Global completion rate
    rate = stats['completion_rate']
    rate_color = success if rate >= 80 else warning if rate >= 50 else Colors.RED
    print(f"{Colors.WHITE}Global completion rate:{Colors.RESET} "
          f"{rate_color}{rate:.1f}%{Colors.RESET}")

    # Category stats
    print(f"{Colors.WHITE}Total unique categories:{Colors.RESET} "
          f"{Colors.CYAN}{stats['unique_categories']}{Colors.RESET}")

    if stats['top_categories']:
        print(info("\nTop 3 most used categories globally:"))
        for idx, (category, count) in enumerate(stats['top_categories'], 1):
            rank_color = Colors.YELLOW if idx == 1 else Colors.GREEN if idx == 2 else Colors.BLUE
            print(f"  {rank_color}{idx}. {Colors.MAGENTA}{category}: {Colors.WHITE}{count} task(s)")


def list_unfinished_tasks_for_user(username):
    """List unfinished (overdue) tasks for a specific user."""
    tasks = get_user_tasks(username)
    unfinished_tasks = get_unfinished_tasks(tasks)

    if not unfinished_tasks:
        print(warning("No unfinished tasks found."))
        return

    # Sort by deadline (most overdue first)
    unfinished_tasks = sort_tasks_by_deadline(unfinished_tasks)

    display_task_list(unfinished_tasks, f"Unfinished Tasks for {username}", include_user=False)

    print(f"\n{Colors.RED}Total unfinished tasks: {len(unfinished_tasks)}{Colors.RESET}")


def list_unfinished_tasks_for_all_users():
    """List unfinished (overdue) tasks for all users."""
    users = load_users()
    all_unfinished = []

    for username in users:
        tasks = get_user_tasks(username)
        unfinished_tasks = get_unfinished_tasks(tasks)
        for task in unfinished_tasks:
            task_with_user = task.copy()
            task_with_user['username'] = username
            all_unfinished.append(task_with_user)

    if not all_unfinished:
        print(warning("No unfinished tasks found for any user."))
        return

    # Sort by deadline (most overdue first)
    all_unfinished = sort_tasks_by_deadline(all_unfinished)

    display_task_list(all_unfinished, "All Unfinished Tasks", include_user=True)

    print(f"\n{Colors.RED}Total unfinished tasks: {len(all_unfinished)}{Colors.RESET}")


def list_pending_tasks_sorted_by_user(username):
    """
    List pending tasks with sorting options for a specific user.

    Args:
        username (str): The username whose pending tasks to list.
    """
    tasks = get_user_tasks(username)
    pending_tasks = get_pending_tasks(tasks)

    if not pending_tasks:
        print(warning("No pending tasks found."))
        return

    print(title("\n--- Pending Tasks ---"))
    print(f"{Colors.CYAN}Choose sorting option:")
    print(f"{Colors.YELLOW}1. {Colors.WHITE}By Priority (High to Low)")
    print(f"{Colors.YELLOW}2. {Colors.WHITE}By Deadline (Earliest first)")
    print(f"{Colors.YELLOW}3. {Colors.WHITE}No sorting (original order)")

    choice = input(prompt("Enter your choice (1-3): ")).strip()

    if choice == "1":
        # Sort by priority (1=High, 2=Medium, 3=Low)
        pending_tasks = sort_tasks_by_priority(pending_tasks)
        print(info("Sorted by priority (High to Low)"))
    elif choice == "2":
        # Sort by deadline
        pending_tasks = sort_tasks_by_deadline(pending_tasks)
        print(info("Sorted by deadline (Earliest first)"))
    elif choice == "3":
        print(info("Original order"))
    else:
        print(warning("Invalid choice, showing in original order"))

    # Display sorted tasks
    display_task_list(pending_tasks, "Pending Tasks", include_user=False)

    # Add pause after displaying tasks
    print(f"\n{Colors.CYAN}Press Enter to continue...")
    input()
